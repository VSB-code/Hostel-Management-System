"""
Allocation Service - Core business logic for room allocation.
"""
import logging
import time
from typing import Tuple, Optional, Dict, Any
from werkzeug.security import generate_password_hash
from models.db import get_db_connection
from services.student_service import create_or_update_student

logger = logging.getLogger(__name__)

def allocate_room(roll_number: str, student_name: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Core allocation logic with Users table support.
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ============================================================
        # STEP 1: USER & STUDENT PROFILE (OUTSIDE MAIN TRANSACTION)
        # ============================================================
        cursor.execute("SELECT id FROM Users WHERE username = %s", (roll_number,))
        user = cursor.fetchone()
        
        if user:
            user_id = user['id']
            # Check existing active allocation
            cursor.execute("""
                SELECT a.allocation_id, r.room_id, h.hostel_name, r.room_number
                FROM Allocations a
                JOIN Rooms r ON a.room_id = r.room_id
                JOIN Hostels h ON r.hostel_id = h.hostel_id
                WHERE a.student_id = %s AND a.status = 'ACTIVE'
            """, (user_id,))
            existing = cursor.fetchone()
            if existing:
                return False, f"❌ Student already allocated to {existing['hostel_name']} - Room {existing['room_number']}", None
        else:
            # Create user
            default_password = generate_password_hash(roll_number)
            email = f"{roll_number}@nitdgp.ac.in"
            cursor.execute("""
                INSERT INTO Users (username, email, password_hash, role, is_active)
                VALUES (%s, %s, %s, 'student', TRUE)
            """, (roll_number, email, default_password))
            user_id = cursor.lastrowid
            conn.commit()
            
            # Create student profile (in a separate call with its own connection)
            create_or_update_student(
                user_id=user_id,
                full_name=student_name,
                roll_number=roll_number,
                email=email
            )
            logger.info(f"Created new user and student profile: {roll_number}")

        # ============================================================
        # STEP 2: ROOM ALLOCATION (IN A FRESH TRANSACTION)
        # ============================================================
        # Close existing cursor/connection and open fresh for allocation
        cursor.close()
        conn.close()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction()

        # Find available room
        cursor.execute("""
            SELECT room_id, hostel_id, room_number, capacity, occupied_count
            FROM Rooms
            WHERE status = 'AVAILABLE' AND occupied_count < capacity
            ORDER BY hostel_id, room_number
            LIMIT 1
        """)
        room = cursor.fetchone()
        if not room:
            conn.rollback()
            return False, "❌ No rooms available in any hostel", None

        room_id = room['room_id']
        new_occupied = room['occupied_count'] + 1
        new_status = 'FULL' if new_occupied == room['capacity'] else 'AVAILABLE'

        # Create allocation
        cursor.execute("""
            INSERT INTO Allocations (student_id, room_id, status)
            VALUES (%s, %s, 'ACTIVE')
        """, (user_id, room_id))

        # Update room
        cursor.execute("""
            UPDATE Rooms 
            SET occupied_count = %s, status = %s 
            WHERE room_id = %s
        """, (new_occupied, new_status, room_id))

        conn.commit()
        logger.info(f"Room {room_id} allocated to student {roll_number}")

        # Fetch hostel details
        cursor.execute("""
            SELECT h.hostel_name, r.room_number
            FROM Rooms r 
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            WHERE r.room_id = %s
        """, (room_id,))
        info = cursor.fetchone()

        return True, f"✅ Success! Allotted {info['hostel_name']} - Room {info['room_number']}", info

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Allocation failed for {roll_number}: {str(e)}", exc_info=True)
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()