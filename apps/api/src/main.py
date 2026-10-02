# This python fiel receives HTTP Requests, routing them to the right function and returning HTTP responses
# How messages communicate

from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine

app = FastAPI(title="UpBank Personal API")

@app.get("/health")
def health_check():
        return {"status": "ok"}