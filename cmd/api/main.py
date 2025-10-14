from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pkg.logger_config import logger
from internal.infrastrucrure.database.session import engine
from internal.infrastrucrure.database.models import Base
import signal
import sys
import asyncio
import os

from internal.handlers.health_check_handler import router as health_router
from internal.handlers.auth_handler import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("initialize of app...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield

    logger.info("initialize shut down succesfully...")

app = FastAPI(
    title="My APP",
    description="Auth by py",
    version="0.01A",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="templates")

app.include_router(health_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def main():
    import uvicorn
    uvicorn.run(
        "cmd.api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info")

    print("server started")
    

if __name__ == "__main__":
    main()