from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

HOST = os.environ.get("HOST")

STATIC_PATH = os.environ.get("STATIC_PATH")

COOKIE = os.environ.get("COOKIE")
X_CSRF_TOKEN = os.environ.get("X-CSRF-Token")
X_REQUESTED_WITH = os.environ.get("X-Requested-With")