import asyncio
from app.db.database import engine

async def test_connection():
    try:
        # Try to connect
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: print("Database connection successful!"))
    except Exception as e:
        print("Database connection failed:", e)

# Run the async function
asyncio.run(test_connection())