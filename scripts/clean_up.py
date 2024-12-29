### clean_up.py

from app import db

# Cleanup script to drop all database tables
def clean_up():
    try:
        print("Starting database cleanup...")
        db.drop_all()
        print("Database cleanup completed successfully.")
    except Exception as e:
        print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    clean_up()
