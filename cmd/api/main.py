from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from pkg.logger_config import get_logger
from internal.infrastrucrure.database.session import engine
from internal.infrastrucrure.database.models import Base
from internal.handlers.health_check_handler import router as health_router
from internal.handlers.auth_handler import router as auth_router

logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("initialize of app...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield

    logger.info("initialize shut down succesfully...")

def main():
    import uvicorn

    uvicorn.run(
        "cmd.api.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info")

app = FastAPI(
    title="My APP",
    description="Auth by py",
    version="0.01A",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")

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

if __name__ == "__main__":
    main()