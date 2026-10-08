import logging
from fastapi import FastAPI
from config import settings, setup_logging
from endpoints import router
import uvicorn

setup_logging()

app = FastAPI(
    title=settings.title
)

app.include_router(router)

logger = logging.getLogger(__name__)
logger.info('Application started')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host=settings.localhost)