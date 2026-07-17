import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """Return a MySQL connection using config."""
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        ssl_disabled=False
    )