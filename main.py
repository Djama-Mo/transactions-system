from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database
import models

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    cash: int

    class Config:
        orm_mode = True


@app.get("/")
async def root():
    return {"message": "Hello"}


db = database.SessionLocal()


@app.put("/input-cash", response_model=User, status_code=200)
def input_cash(user_id: int, cash: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.cash = user.cash + cash
    db.commit()
    return user


@app.put("/output-cash", response_model=User, status_code=200)
def output_cash(user_id: int, cash: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.cash < cash:
        raise HTTPException(status_code=400, detail="Not enough funds")
    user.cash = user.cash - cash
    db.commit()
    return user


@app.post("/create-user", response_model=User, status_code=201)
def create_user(user: User):
    new_user = models.User(
        name=user.name,
        cash=user.cash
    )

    db_item = db.query(models.User).filter(user.name == new_user.name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="User already exists")

    db.add(new_user)
    db.commit()

    return new_user
