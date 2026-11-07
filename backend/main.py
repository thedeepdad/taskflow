from fastapi.middleware.cors import CORSMiddleware
from config import settings, setup_logging
from endpoints import router
from fastapi import FastAPI
from rabbit.lifespan import lifespan
from granian import Granian
from granian.constants import Interfaces
import logging

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
    server = Granian(
        target="main:app",
        address=settings.localhost,
        port=8000,
        interface=Interfaces.ASGI,
        workers=1,
        reload=True
    )

    server.serve()
