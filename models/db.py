import os
import mysql.connector
from config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA_PATH = os.path.join(BASE_DIR, "certs", "ca.pem")

def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        ssl_ca=CA_PATH,
        use_pure=True
    )