import time

from fastapi import HTTPException
from pydantic import BaseModel

import database
import models


db = database.SessionLocal()


class User(BaseModel):
    name: str
    cash: int

    class Config:
        orm_mode = True


def input_cash(user_id: int, cash: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    time.sleep(5)
    user.cash = user.cash + cash
    db.commit()
    return orm_model_to_dict(user)


def output_cash(user_id: int, cash: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    time.sleep(10)
    if user.cash < cash:
        raise HTTPException(status_code=400, detail="Not enough funds")
    user.cash = user.cash - cash
    db.commit()
    return orm_model_to_dict(user)


def create_user(user: User):
    new_user = models.User(
        name=user.name,
        cash=user.cash
    )

    db_item = db.query(models.User).filter(models.User.name == new_user.name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="User already exists")

    db.add(new_user)
    db.commit()

    return new_user


def orm_model_to_dict(model):
    result = {}
    for column in model.__table__.columns:
        result[column.name] = str(getattr(model, column.name))

    return result
