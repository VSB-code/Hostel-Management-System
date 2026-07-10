from flask import Blueprint, render_template
from services.room_service import get_all_rooms_grouped
from models.db import get_db_connection

room_bp = Blueprint('room', __name__)

@room_bp.route('/')
def rooms_page():
    grouped_rooms = get_all_rooms_grouped()
    # Also fetch hostels list for dropdown if needed
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Hostels ORDER BY hostel_name")
    hostels = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('rooms.html', hostels=hostels, grouped_rooms=grouped_rooms)