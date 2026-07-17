import re
from models.db import get_db_connection


def is_valid_roll_number(roll):
    return bool(re.match(r'^\d{2}[A-Z]{2}\d{4}$', roll))


def create_or_update_student(student_id, student_name, roll_number=None, email=None):
    if not student_name:
        raise ValueError('student_name is required')
    if not roll_number:
        raise ValueError('roll_number is required')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Students (student_id, roll_number, full_name, email)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                roll_number = VALUES(roll_number),
                full_name = VALUES(full_name),
                email = VALUES(email)
        """, (student_id, roll_number, student_name, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()