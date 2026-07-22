from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.db import get_db_connection
from mysql.connector import Error
from .admin_routes import login_required  # Reuse admin's login decorator

# Create blueprint
allocation_bp = Blueprint('allocation', __name__, url_prefix='/allocations')

# ============================================================
# PAGE: View All Allocations (Admin Only)
# ============================================================
@allocation_bp.route('/')
@login_required 
def view_allocations():
    """
    Display complete allocation history (active + vacated) 
    with server-side rendering
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
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
        return render_template('allocations.html', allocations=allocations)
    except Error as e:
        flash(f'Error loading allocations: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    finally:
        cursor.close()
        conn.close()

# ============================================================
# API: JSON data for Allocations (For frontend JS - optional)
# ============================================================
@allocation_bp.route('/api')
@login_required
def api_allocations():
    """
    JSON endpoint for allocations data.
    Used by allocations.js for dynamic search/filter (future enhancement)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
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
        
        # Convert datetime objects to string for JSON serialization
        for alloc in allocations:
            if alloc['allocated_at']:
                alloc['allocated_at'] = alloc['allocated_at'].isoformat()
            if alloc['vacated_at']:
                alloc['vacated_at'] = alloc['vacated_at'].isoformat()
                
        return jsonify({"success": True, "data": allocations})
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()