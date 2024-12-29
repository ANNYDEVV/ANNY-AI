### seed_data.py

from app import db
from app.models import Staker, RevenuePool

# Seeding script to populate the database with initial data
def seed():
    try:
        print("Starting data seeding...")
        # Add initial staker data
        staker1 = Staker(address="0xABC123", staked_amount=100.0, rewards=0.0)
        staker2 = Staker(address="0xDEF456", staked_amount=200.0, rewards=0.0)

        db.session.add_all([staker1, staker2])

        # Add initial revenue pool data
        revenue_pool = RevenuePool(total_revenue=0.0)
        db.session.add(revenue_pool)

        db.session.commit()
        print("Data seeding completed successfully.")
    except Exception as e:
        print(f"Data seeding failed: {e}")

if __name__ == "__main__":
    seed()
