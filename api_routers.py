from fastapi import APIRouter
from starlette.responses import JSONResponse

from celery_tasks import input_cash_task, output_cash_task
from db_api import User, create_user

router = APIRouter(prefix='/funds', tags=['Fund'], responses={404: {"description": "Not found"}})


@router.post("/input-cash")
async def input_cash(user_id: int, cash: int):
    task = input_cash_task.s(user_id, cash).apply_async()
    return JSONResponse({"task_id": task.get(disable_sync_subtasks=False)})


@router.post("/output-cash")
async def input_cash(user_id: int, cash: int):
    task = output_cash_task.s(user_id, cash).apply_async()
    return JSONResponse({"task_id": task.get(disable_sync_subtasks=False)})


@router.post("/create-user")
async def create_user(user: User):
    return create_user(user)
