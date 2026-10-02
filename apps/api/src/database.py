# This allows us to talk to Postgres


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.DATABASE_URL) # the connection to the postgres database
SessionLocal = sessionmaker(bind=engine) # a factory to create sessions to read and write data

with engine.connect() as conn:
    conn.execute(text("SELECT 1"))