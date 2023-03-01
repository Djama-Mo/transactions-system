import time

from fastapi import HTTPException
from pydantic import BaseModel

from database.database_engine import SessionLocal
from database.models import User as UserModel


db = SessionLocal()


class User(BaseModel):
    name: str
    cash: int

    class Config:
        orm_mode = True


def input_cash(user_id: int, cash: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    time.sleep(5)
    user.cash = user.cash + cash
    db.commit()
    return orm_model_to_dict(user)


def output_cash(user_id: int, cash: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    time.sleep(10)
    if user.cash < cash:
        raise HTTPException(status_code=400, detail="Not enough funds")
    user.cash = user.cash - cash
    db.commit()
    return orm_model_to_dict(user)


def create_user(user: User):
    new_user = UserModel(
        name=user.name,
        cash=user.cash
    )

    db_item = db.query(UserModel).filter(UserModel.name == new_user.name).first()
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
