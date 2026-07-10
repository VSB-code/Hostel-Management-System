from models.db import get_db_connection

def find_available_room():
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
    cursor.close()
    conn.close()
    return room

def update_room_occupancy(room_id, new_occupied, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Rooms SET occupied_count = %s, status = %s WHERE room_id = %s
    """, (new_occupied, new_status, room_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_room_details(room_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT h.hostel_name, r.room_number
        FROM Rooms r JOIN Hostels h ON r.hostel_id = h.hostel_id
        WHERE r.room_id = %s
    """, (room_id,))
    info = cursor.fetchone()
    cursor.close()
    conn.close()
    return info

def get_all_rooms_grouped():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.room_id, r.hostel_id, h.hostel_name, r.room_number,
               r.floor_number, r.capacity, r.occupied_count, r.status
        FROM Rooms r JOIN Hostels h ON r.hostel_id = h.hostel_id
        ORDER BY h.hostel_name, r.room_number
    """)
    all_rooms = cursor.fetchall()
    grouped = {}
    for room in all_rooms:
        h_name = room['hostel_name']
        grouped.setdefault(h_name, []).append(room)
    cursor.close()
    conn.close()
    return grouped