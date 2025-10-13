from fastapi import FastAPI
from contextlib import asynccontextmanager
import signal
import sys
import asyncio

app = FastAPI(
    title="My APP",
    description="Auth by py",
    version="0.01A"
)

@app.get("/")
async def root():
    return {
        "message": "SoundTube API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/register")
async def register():
    return {"message": "Register"}

@app.post("/login")
async def login():
    return {"message": "Login"}

@app.delete("/logout")
async def logout():
    return {"message": "Logout"}

def main():
    print("Server started")

if __name__ == "__main__":
    main()