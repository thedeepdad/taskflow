from fastapi.middleware.cors import CORSMiddleware
from config import settings, setup_logging
from endpoints import router
from fastapi import FastAPI
from rabbit.lifespan import lifespan
import logging
import uvicorn

setup_logging()

app = FastAPI(
    title=settings.title,
    lifespan=lifespan
)

app.include_router(router)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

logger = logging.getLogger(__name__)
logger.info('Application started')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host=settings.localhost)
