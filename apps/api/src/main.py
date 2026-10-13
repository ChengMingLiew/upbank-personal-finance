# This python fiel receives HTTP Requests, routing them to the right function and returning HTTP responses
# How messages communicate

from fastapi import FastAPI
from src.routers import auth, connections, sync, accounts, transactions

app = FastAPI(title="UpBank Personal API")

@app.get("/health")
def health_check():
        return {"status": "ok"}

app.include_router(auth.router, tags=["auth"])
app.include_router(connections.router, prefix="/connections", tags=["connections"])
app.include_router(sync.router, prefix="/sync", tags=["sync"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])