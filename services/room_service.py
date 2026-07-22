"""
Room Service - All room-related database operations.
Handles: Finding available rooms, updating occupancy, grouping rooms.
"""
import logging
from typing import Optional, Dict, List, Any
from models.db import get_db_connection

logger = logging.getLogger(__name__)

def find_available_room() -> Optional[Dict[str, Any]]:
    """
    Find the first available room across all hostels.
    
    Returns:
        Optional[Dict]: Room details if found, None otherwise.
            Keys: room_id, hostel_id, room_number, capacity, occupied_count
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT room_id, hostel_id, room_number, capacity, occupied_count
            FROM Rooms
            WHERE status = 'AVAILABLE' AND occupied_count < capacity
            ORDER BY hostel_id, room_number
            LIMIT 1
        """)
        room = cursor.fetchone()
        
        if room:
            logger.debug(f"Found available room: {room['room_id']}")
        else:
            logger.debug("No available rooms found")
            
        return room
        
    except Exception as e:
        logger.error(f"Error finding available room: {str(e)}", exc_info=True)
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_room_occupancy(room_id: int, new_occupied: int, new_status: str) -> None:
    """
    Update room occupancy count and status.
    
    Args:
        room_id (int): Room ID to update
        new_occupied (int): New occupied count
        new_status (str): New status ('AVAILABLE' or 'FULL')
        
    Raises:
        Exception: If update fails
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE Rooms 
            SET occupied_count = %s, status = %s 
            WHERE room_id = %s
        """, (new_occupied, new_status, room_id))
        
        conn.commit()
        logger.debug(f"Updated room {room_id}: occupied={new_occupied}, status={new_status}")
        
    except Exception as e:
        logger.error(f"Error updating room {room_id}: {str(e)}", exc_info=True)
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_room_details(room_id: int) -> Optional[Dict[str, Any]]:
    """
    Get room details with hostel name.
    
    Args:
        room_id (int): Room ID
        
    Returns:
        Optional[Dict]: Room details with hostel_name and room_number
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT h.hostel_name, r.room_number
            FROM Rooms r 
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            WHERE r.room_id = %s
        """, (room_id,))
        info = cursor.fetchone()
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting room details for {room_id}: {str(e)}", exc_info=True)
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_rooms_grouped() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all rooms grouped by hostel name.
    
    Returns:
        Dict[str, List[Dict]]: Hostel name -> List of room dicts
            Room dict keys: room_id, hostel_id, hostel_name, room_number,
                           floor_number, capacity, occupied_count, status
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT r.room_id, r.hostel_id, h.hostel_name, r.room_number,
                   r.floor_number, r.capacity, r.occupied_count, r.status
            FROM Rooms r 
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            ORDER BY h.hostel_name, r.room_number
        """)
        all_rooms = cursor.fetchall()
        
        grouped = {}
        for room in all_rooms:
            h_name = room['hostel_name']
            if h_name not in grouped:
                grouped[h_name] = []
            grouped[h_name].append(room)
        
        logger.debug(f"Grouped {len(all_rooms)} rooms into {len(grouped)} hostels")
        return grouped
        
    except Exception as e:
        logger.error(f"Error getting grouped rooms: {str(e)}", exc_info=True)
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()