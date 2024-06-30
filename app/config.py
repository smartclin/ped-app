import os

# Flask App Configuration
DEBUG = True  # Set to False in production
SECRET_KEY = "your_secret_key_here"  # Change this to a random secret key

# Database Configuration
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL", "postgresql://drhazem:Health@localhost:5432/smart"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CORS Configuration
CORS_HEADERS = "Content-Type"
