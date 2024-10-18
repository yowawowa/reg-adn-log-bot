from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

# Create an engine to connect to the database.
# The URL is constructed from the configuration settings.

async_engine = create_async_engine(
    url=settings.DB_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

