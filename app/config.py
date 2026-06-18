import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))
REFRESH_TOKEN_EXPIRE_DAYS =int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS","7"))
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")

BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")
FRONTEND_RESET_PASSWORD_URL = os.getenv(
    "FRONTEND_RESET_PASSWORD_URL",
    "http://localhost:3000/reset-password"
)
FRONTEND_VERIFY_EMAIL_URL = os.getenv(
    "FRONTEND_VERIFY_EMAIL_URL",
    "http://localhost:3000/verify-email"
)
MAX_FAILED_LOGIN_ATTEMPTS = os.getenv(
    "MAX_FAILED_LOGIN_ATTEMPTS",
    "5"
)

ACCOUNT_LOCKOUT_MINUTES = os.getenv(
    "ACCOUNT_LOCKOUT_MINUTES",
    "15"
)
CORS_ORIGINS = [
    origin.strip()
    for origin in BACKEND_CORS_ORIGINS.split(",")
    if origin.strip()
]