### migrate_db.py

from app import db

# Migration script to create all database tables
def migrate():
    try:
        print("Starting database migration...")
        db.create_all()
        print("Database migration completed successfully.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
