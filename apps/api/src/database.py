# This allows us to talk to Postgres


from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(settings.DATABASE_URL) # the connection to the postgres database
SessionLocal = sessionmaker(bind=engine) # a factory to create sessions to read and write data

async_engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session():

    async with AsyncSessionLocal() as session:
        yield session