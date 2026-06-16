from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re

import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this-in-production'  

load_dotenv()

# --------------------- Database Connection ---------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
# --------------------- Helper Functions ---------------------
def is_valid_roll_number(roll):
    # NIT Durgapur ke typical roll format: 24CS1001
    return bool(re.match(r'^\d{2}[A-Z]{2}\d{4}$', roll))

# --------------------- Admin Login Decorator ---------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login first', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------- Routes ---------------------
@app.route('/')
def index():
    """Student frontend page"""
    return render_template('index.html')
        

@app.route('/book', methods=['POST'])
def book_room():
    """Allocate a room to a student (first-come-first-serve)"""
    student_id = request.form.get('student_id', '').strip()
    student_name = request.form.get('student_name', '').strip()
    
    if not student_id or not student_name:
        return "❌ Student ID and Name are required", 400
    
    if not is_valid_roll_number(student_id):
        return "❌ Invalid roll number format (e.g., 24CS1001)", 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Check if student already has an ACTIVE allocation
        cursor.execute("""
            SELECT a.allocation_id, r.room_id, h.hostel_name, r.room_number
            FROM Allocations a
            JOIN Rooms r ON a.room_id = r.room_id
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            WHERE a.student_id = %s AND a.status = 'ACTIVE'
        """, (student_id,))
        existing = cursor.fetchone()
        if existing:
            return f"❌ Student already allocated to {existing['hostel_name']} - Room {existing['room_number']}", 409
        
        # 2. Find first available room (occupied_count < capacity AND status='AVAILABLE')
        cursor.execute("""
            SELECT room_id, hostel_id, room_number, capacity, occupied_count
            FROM Rooms
            WHERE status = 'AVAILABLE' AND occupied_count < capacity
            ORDER BY hostel_id, room_number
            LIMIT 1
        """)
        room = cursor.fetchone()
        if not room:
            return "❌ No rooms available in any hostel", 404
        
        room_id = room['room_id']
        new_occupied = room['occupied_count'] + 1
        
#  just 
        
        # 4. Insert or update student in Students table
        cursor.execute("""
            INSERT INTO Students (student_id, student_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE student_name = VALUES(student_name)
        """, (student_id, student_name))
        
        # 5. Create allocation record
        cursor.execute("""
            INSERT INTO Allocations (student_id, room_id, status)
            VALUES (%s, %s, 'ACTIVE')
        """, (student_id, room_id))
        
        # 6. Update room occupancy and possibly status
        new_status = 'FULL' if new_occupied == room['capacity'] else 'AVAILABLE'
        cursor.execute("""
            UPDATE Rooms
            SET occupied_count = %s, status = %s
            WHERE room_id = %s
        """, (new_occupied, new_status, room_id))
        
        conn.commit()
        
        # 7. Fetch hostel name for success message
        cursor.execute("""
            SELECT h.hostel_name, r.room_number
            FROM Rooms r
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            WHERE r.room_id = %s
        """, (room_id,))
        info = cursor.fetchone()
        
        return f"✅ Success! Allotted {info['hostel_name']} - Room {info['room_number']}"
        
    except Error as e:
        conn.rollback()
        return f"⚠️ Database error: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/occupancy')
def api_occupancy():
    """JSON endpoint for live occupancy stats (used by frontend)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                h.hostel_id,
                h.hostel_name,
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

@app.route('/status')
def status_page():
    """Full page with detailed occupancy table"""
    return render_template('status.html')


# /  room route
@app.route('/rooms')
def rooms_page():
    """Fetches all rooms grouped by their respective hostels for visualization"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch hostels list to populate navigation tabs or drop-downs
        cursor.execute("SELECT * FROM Hostels ORDER BY hostel_name")
        hostels = cursor.fetchall()

        # Fetch all rooms with their structural hostel name mapped via inner join
        cursor.execute("""
            SELECT r.room_id, r.hostel_id, h.hostel_name, r.room_number, 
                   r.floor_number, r.capacity, r.occupied_count, r.status
            FROM Rooms r
            JOIN Hostels h ON r.hostel_id = h.hostel_id
            ORDER BY h.hostel_name, r.room_number
        """)
        all_rooms = cursor.fetchall()

        # Interview Ready Optimization: Grouping rooms by hostel_name in a Python dictionary
        grouped_rooms = {}
        for room in all_rooms:
            h_name = room['hostel_name']
            if h_name not in grouped_rooms:
                grouped_rooms[h_name] = []
            grouped_rooms[h_name].append(room)

        return render_template('rooms.html', hostels=hostels, grouped_rooms=grouped_rooms)

    except Error as e:
        return f"⚠️ Database query execution crash: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()
        
        
# --------------------- Admin Routes ---------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Admins WHERE username = %s", (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard showing all active allocations"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all active allocations with student & room details
    cursor.execute("""
        SELECT a.allocation_id, a.allocated_at, 
               s.student_id, s.student_name,
               h.hostel_name, r.room_number, r.floor_number
        FROM Allocations a
        JOIN Students s ON a.student_id = s.student_id
        JOIN Rooms r ON a.room_id = r.room_id
        JOIN Hostels h ON r.hostel_id = h.hostel_id
        WHERE a.status = 'ACTIVE'
        ORDER BY a.allocated_at DESC
    """)
    allocations = cursor.fetchall()
    
    # Summary stats
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT a.student_id) AS total_students,
            (SELECT COUNT(*) FROM Rooms WHERE status = 'AVAILABLE') AS available_rooms,
            (SELECT COUNT(*) FROM Rooms WHERE status = 'FULL') AS full_rooms,
            (SELECT COUNT(*) FROM Rooms WHERE status = 'MAINTENANCE') AS maintenance_rooms
        FROM Allocations a WHERE a.status = 'ACTIVE'
    """)
    summary = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_dashboard.html', 
                           allocations=allocations, 
                           summary=summary)

@app.route('/admin/vacate/<int:allocation_id>', methods=['POST'])
@login_required
def vacate_room(allocation_id):
    """Mark an allocation as VACATED and free up the room"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        conn.start_transaction()
        
        # Get room_id from allocation
        cursor.execute("SELECT room_id FROM Allocations WHERE allocation_id = %s AND status = 'ACTIVE'", (allocation_id,))
        alloc = cursor.fetchone()
        if not alloc:
            flash('Allocation not found or already vacated', 'error')
            return redirect(url_for('admin_dashboard'))
        
        room_id = alloc['room_id']
        
        # Update allocation status to VACATED with vacated_at timestamp
        cursor.execute("""
            UPDATE Allocations
            SET status = 'VACATED', vacated_at = CURRENT_TIMESTAMP
            WHERE allocation_id = %s
        """, (allocation_id,))
        
        # Decrement room occupied_count and update status if needed
        cursor.execute("""
            UPDATE Rooms
            SET occupied_count = occupied_count - 1,
                status = CASE 
                            WHEN occupied_count - 1 < capacity THEN 'AVAILABLE'
                            ELSE status
                         END
            WHERE room_id = %s
        """, (room_id,))
        
        conn.commit()
        flash('Room vacated successfully', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset_all', methods=['POST'])
@login_required
def reset_all():
    """DANGER: Reset entire system - delete all allocations, reset rooms"""
    if request.form.get('confirm') != 'YES':
        flash('Type "YES" to confirm reset', 'error')
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        # Delete all allocations
        cursor.execute("DELETE FROM Allocations")
        # Reset rooms
        cursor.execute("UPDATE Rooms SET occupied_count = 0, status = 'AVAILABLE'")
        conn.commit()
        flash('System reset successful. All rooms are now free.', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Reset failed: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

# --------------------- Run App ---------------------
if __name__ == '__main__':
    app.run(debug=True)
