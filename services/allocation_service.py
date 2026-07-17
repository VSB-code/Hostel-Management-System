from models.db import get_db_connection
from services.student_service import create_or_update_student
from werkzeug.security import generate_password_hash
import re

def allocate_room(roll_number, student_name):
    """Core allocation logic with Users table support"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        conn.start_transaction()
        
        # 1. Check if student exists in Users table
        cursor.execute("SELECT id FROM Users WHERE username = %s", (roll_number,))
        user = cursor.fetchone()
        
        if user:
            user_id = user['id']
            # Check if already has active allocation
            cursor.execute("""
                SELECT a.allocation_id, r.room_id, h.hostel_name, r.room_number
                FROM Allocations a
                JOIN Rooms r ON a.room_id = r.room_id
                JOIN Hostels h ON r.hostel_id = h.hostel_id
                WHERE a.student_id = %s AND a.status = 'ACTIVE'
            """, (user_id,))
            existing = cursor.fetchone()
            if existing:
                return False, f"Student already allocated to {existing['hostel_name']} - Room {existing['room_number']}", None
        else:
            # Create new user with default password (roll number as default)
            # In production, send email with OTP/password reset link
            default_password = generate_password_hash(roll_number)
            cursor.execute("""
                INSERT INTO Users (username, email, password_hash, role, is_active)
                VALUES (%s, %s, %s, 'student', TRUE)
            """, (roll_number, f"{roll_number}@nitdgp.ac.in", default_password))
            user_id = cursor.lastrowid
            
            # Create or update student profile
            create_or_update_student(
                user_id,
                student_name,
                roll_number=roll_number,
                email=f"{roll_number}@nitdgp.ac.in"
            )
        
        # 2. Find available room
        cursor.execute("""
            SELECT room_id, hostel_id, room_number, capacity, occupied_count
            FROM Rooms
            WHERE status = 'AVAILABLE' AND occupied_count < capacity
            ORDER BY hostel_id, room_number
            LIMIT 1
        """)
        room = cursor.fetchone()
        if not room:
            return False, "No rooms available in any hostel", None
        
        room_id = room['room_id']
        new_occupied = room['occupied_count'] + 1
        new_status = 'FULL' if new_occupied == room['capacity'] else 'AVAILABLE'
        
        # 3. Create allocation
        cursor.execute("""
            INSERT INTO Allocations (student_id, room_id, status)
            VALUES (%s, %s, 'ACTIVE')
        """, (user_id, room_id))
        
        # 4. Update room
        cursor.execute("""
            UPDATE Rooms SET occupied_count = %s, status = %s WHERE room_id = %s
        """, (new_occupied, new_status, room_id))
        
        conn.commit()
        
        # 5. Fetch hostel name
        cursor.execute("""
            SELECT h.hostel_name, r.room_number
            FROM Rooms r JOIN Hostels h ON r.hostel_id = h.hostel_id
            WHERE r.room_id = %s
        """, (room_id,))
        info = cursor.fetchone()
        
        return True, f"Success! Allotted {info['hostel_name']} - Room {info['room_number']}", info
        
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()