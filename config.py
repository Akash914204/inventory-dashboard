import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'invuser'),
    'password': os.getenv('DB_PASS', 'invpass'),
    'database': os.getenv('DB_NAME', 'inventory_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}
