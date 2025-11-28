import asyncio
from app.db.database import engine
from app.models.base import Base
from app.models.user import User, Event  # Import all models

async def create_tables():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
