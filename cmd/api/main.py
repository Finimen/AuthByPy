from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pkg.logger_config import logger
import signal
import sys
import asyncio
import os

from internal.handlers.health_check_handler import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("initialize of app...")

    yield

    logger.info("initialize shut down succesfully...")

app = FastAPI(
    title="My APP",
    description="Auth by py",
    version="0.01A",
    lifespan=lifespan
)

app.include_router(health_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    print("server started")

if __name__ == "__main__":
    main()