from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
from functools import wraps
from models.db import get_db_connection
from mysql.connector import Error

admin_bp = Blueprint('admin', __name__)

# -------------------- Login Decorator --------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login first', 'error')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated

# -------------------- Admin Login (Using `Users` table) --------------------
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Query from `Users` table and filter by role = 'admin'
        cursor.execute("""
            SELECT id, username, password_hash, role 
            FROM Users 
            WHERE username = %s AND role = 'admin' AND is_active = TRUE
        """, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = user['username']
            session['admin_id'] = user['id']
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

# -------------------- Admin Logout --------------------
@admin_bp.route('/logout')
def admin_logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('admin.admin_login'))

# -------------------- Admin Dashboard --------------------
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Active allocations (using Users table for student name)
    cursor.execute("""
        SELECT a.allocation_id, a.allocated_at,
               u.username AS student_id, 
               s.full_name AS student_name,
               h.hostel_name, r.room_number, r.floor_number
        FROM Allocations a
        JOIN Users u ON a.student_id = u.id
        JOIN Students s ON u.id = s.student_id
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
    return render_template('admin_dashboard.html', allocations=allocations, summary=summary)

# ============================================================
# REST OF THE ROUTES (vacate, reset_all, students, allocations)
# Stay the same, just update student_id mapping from INT to VARCHAR
# ============================================================

# -------------------- Vacate Room --------------------
@admin_bp.route('/vacate/<int:allocation_id>', methods=['POST'])
@login_required
def vacate_room(allocation_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cursor.execute("SELECT room_id FROM Allocations WHERE allocation_id = %s AND status = 'ACTIVE'", (allocation_id,))
        alloc = cursor.fetchone()
        if not alloc:
            flash('Allocation not found or already vacated', 'error')
            return redirect(url_for('admin.admin_dashboard'))
        room_id = alloc['room_id']
        
        cursor.execute("""
            UPDATE Allocations SET status = 'VACATED', vacated_at = CURRENT_TIMESTAMP
            WHERE allocation_id = %s
        """, (allocation_id,))
        cursor.execute("""
            UPDATE Rooms
            SET occupied_count = occupied_count - 1,
                status = CASE WHEN occupied_count - 1 < capacity THEN 'AVAILABLE' ELSE status END
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
    return redirect(url_for('admin.admin_dashboard'))

# -------------------- Reset System --------------------
@admin_bp.route('/reset_all', methods=['POST'])
@login_required
def reset_all():
    if request.form.get('confirm') != 'YES':
        flash('Type "YES" to confirm reset', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("DELETE FROM Allocations")
        cursor.execute("UPDATE Rooms SET occupied_count = 0, status = 'AVAILABLE'")
        conn.commit()
        flash('System reset successful. All rooms are now free.', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Reset failed: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin.admin_dashboard'))

# -------------------- View All Students (Updated) --------------------
@admin_bp.route('/students')
@login_required
def students_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            u.id AS user_id,
            u.username AS roll_number,
            s.full_name AS student_name,
            s.email,
            u.created_at,
            a.status AS allocation_status,
            a.allocated_at,
            a.vacated_at,
            h.hostel_name,
            r.room_number
        FROM Users u
        JOIN Students s ON u.id = s.student_id
        LEFT JOIN (
            SELECT * FROM Allocations 
            WHERE allocation_id IN (
                SELECT MAX(allocation_id) 
                FROM Allocations 
                GROUP BY student_id
            )
        ) a ON u.id = a.student_id
        LEFT JOIN Rooms r ON a.room_id = r.room_id
        LEFT JOIN Hostels h ON r.hostel_id = h.hostel_id
        WHERE u.role = 'student'
        ORDER BY u.username
    """)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

# -------------------- View All Allocations (Updated) --------------------
@admin_bp.route('/allocations')
@login_required
def allocations_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            a.allocation_id,
            u.username AS student_id,
            s.full_name AS student_name,
            h.hostel_name,
            r.room_number,
            a.status,
            a.allocated_at,
            a.vacated_at
        FROM Allocations a
        JOIN Users u ON a.student_id = u.id
        JOIN Students s ON u.id = s.student_id
        JOIN Rooms r ON a.room_id = r.room_id
        JOIN Hostels h ON r.hostel_id = h.hostel_id
        ORDER BY a.allocated_at DESC
    """)
    allocations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allocations.html', allocations=allocations)