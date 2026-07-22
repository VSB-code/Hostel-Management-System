"""
Student Service - All student-related operations.
Handles: Roll number validation, creating/updating student profiles.
"""
import re
import logging
import time
from typing import Optional, Dict, Any
from models.db import get_db_connection

logger = logging.getLogger(__name__)

ROLL_NUMBER_PATTERN = r'^\d{2}[A-Z]{2}\d{4}$'
MAX_NAME_LENGTH = 100

def is_valid_roll_number(roll: str) -> bool:
    """Validate NIT Durgapur roll number format: 24CS1001"""
    if not roll or not isinstance(roll, str):
        return False
    return bool(re.match(ROLL_NUMBER_PATTERN, roll.strip()))

def create_or_update_student(
    user_id: int,
    full_name: str,
    roll_number: Optional[str] = None,
    email: Optional[str] = None,
    max_retries: int = 3
) -> None:
    """
    Create or update student profile with retry logic for lock timeouts.
    
    Args:
        user_id (int): User ID (foreign key to Users.id)
        full_name (str): Full name of student
        roll_number (Optional[str]): Roll number
        email (Optional[str]): Email address
        max_retries (int): Number of retry attempts for lock timeout
    """
    if not full_name or not full_name.strip():
        raise ValueError("full_name is required")
    if not roll_number or not roll_number.strip():
        raise ValueError("roll_number is required")
    if not is_valid_roll_number(roll_number):
        raise ValueError(f"Invalid roll_number format: {roll_number}")

    full_name = full_name.strip()
    roll_number = roll_number.strip()
    email = (email or "").strip().lower() or f"{roll_number}@nitdgp.ac.in"

    last_exception = None
    for attempt in range(max_retries):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Students (student_id, roll_number, full_name, email)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    roll_number = VALUES(roll_number),
                    full_name = VALUES(full_name),
                    email = VALUES(email)
            """, (user_id, roll_number, full_name, email))
            conn.commit()
            logger.info(f"Student profile created/updated: {roll_number} (user_id: {user_id})")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.warning(f"Student upsert attempt {attempt+1} failed for {roll_number}: {str(e)}")
            last_exception = e
            if "Lock wait timeout" in str(e) and attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                continue
            raise last_exception

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    if last_exception:
        raise last_exception