import re
from models.db import get_db_connection

def is_valid_roll_number(roll):
    return bool(re.match(r'^\d{2}[A-Z]{2}\d{4}$', roll))

def create_or_update_student(student_id, student_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Students (student_id, student_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE student_name = VALUES(student_name)
    """, (student_id, student_name))
    conn.commit()
    cursor.close()
    conn.close()