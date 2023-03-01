from fastapi import FastAPI

from celery_utils import create_celery
from api_routers import router


def create_app() -> FastAPI:
    current_app = FastAPI()

    current_app.celery_app = create_celery()
    current_app.include_router(router)
    return current_app


app = create_app()
celery = app.celery_app


@app.get("/")
async def root():
    return {"message": "Hello"}
