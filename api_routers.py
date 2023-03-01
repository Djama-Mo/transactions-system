from fastapi import APIRouter
from starlette.responses import JSONResponse

from celery_settings.celery_tasks import input_cash_task, output_cash_task
from database import db_api
from celery_settings.celery_utils import get_task_info

router = APIRouter(prefix='/funds', tags=['Fund'], responses={404: {"description": "Not found"}})


@router.post("/input-cash")
async def input_cash(user_id: int, cash: int):
    task = input_cash_task.apply_async(kwargs={"user_id": user_id, "cash": cash})
    return JSONResponse({"task_id": task.id})


@router.post("/output-cash")
async def output_cash(user_id: int, cash: int):
    task = output_cash_task.delay(user_id, cash)
    return JSONResponse({"task_id": task.id})


@router.post("/create-user")
async def create_user(user: db_api.User):
    return db_api.create_user(user)


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    return get_task_info(task_id)