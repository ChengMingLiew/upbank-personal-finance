import os

os.environ.setdefault("ENCRYPTION_KEY", "00" * 32)
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")