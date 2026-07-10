from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from services.allocation_service import allocate_room
from services.student_service import is_valid_roll_number
from services.room_service import get_all_rooms_grouped
from models.db import get_db_connection
from mysql.connector import Error

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
def index():
    return render_template('index.html')

@student_bp.route('/book', methods=['POST'])
def book_room():
    roll_number = request.form.get('student_id', '').strip()  # roll number from form
    student_name = request.form.get('student_name', '').strip()
    
    if not roll_number or not student_name:
        return "❌ Student ID and Name are required", 400
    if not is_valid_roll_number(roll_number):
        return "❌ Invalid roll number format (e.g., 24CS1001)", 400

    try:
        # allocate_room will handle:
        # 1. Check if user exists in Users table, if not create one with role='student'
        # 2. Check/update Students profile
        # 3. Allocate room
        success, message, _ = allocate_room(roll_number, student_name)
        if success:
            return message, 200
        else:
            return message, 409
    except Exception as e:
        return f"⚠️ Error: {str(e)}", 500

@student_bp.route('/status')
def status_page():
    return render_template('status.html')

@student_bp.route('/api/occupancy')
def api_occupancy():
    # Same as before, doesn't touch Users table
    from models.db import get_db_connection
    from mysql.connector import Error
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT h.hostel_id, h.hostel_name,
                   COUNT(r.room_id) AS total_rooms,
                   SUM(r.capacity) AS total_beds,
                   SUM(r.occupied_count) AS occupied_beds,
                   SUM(r.capacity) - SUM(r.occupied_count) AS available_beds
            FROM Hostels h
            JOIN Rooms r ON h.hostel_id = r.hostel_id
            GROUP BY h.hostel_id
            ORDER BY h.hostel_id
        """)
        stats = cursor.fetchall()
        return jsonify({"success": True, "stats": stats})
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/rooms')
def rooms_page():
    # Same as before
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Hostels ORDER BY hostel_name")
        hostels = cursor.fetchall()

        cursor.execute("""
            SELECT r.room_id, r.hostel_id, h.hostel_name, r.room_number,
                   r.floor_number, r.capacity, r.occupied_count, r.status
            FROM Rooms r
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            ORDER BY h.hostel_name, r.room_number
        """)
        all_rooms = cursor.fetchall()

        grouped_rooms = {}
        for room in all_rooms:
            h_name = room['hostel_name']
            if h_name not in grouped_rooms:
                grouped_rooms[h_name] = []
            grouped_rooms[h_name].append(room)

        return render_template('rooms.html', hostels=hostels, grouped_rooms=grouped_rooms)

    except Error as e:
        return f"⚠️ Database error: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()