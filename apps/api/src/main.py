# This python fiel receives HTTP Requests, routing them to the right function and returning HTTP responses
# How messages communicate

from fastapi import FastAPI
from src.routers import auth, connections

app = FastAPI(title="UpBank Personal API")

@app.get("/health")
def health_check():
        return {"status": "ok"}

app.include_router(auth.router, tags=["auth"])
app.include_router(connections.router, prefix="/connections", tags=["connections"])