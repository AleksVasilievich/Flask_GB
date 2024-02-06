import datetime
from typing import List


import databases
import pandas as pd
import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from flask import request
# from requests import request
# from flask import request
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

DATABASE_URL = "sqlite:///shop1.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
templates = Jinja2Templates(directory="./templates")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    surname = Column(String(40))
    email = Column(String(120))
    password = Column(String(5))

    orders = relationship("Order", back_populates="user")


class UserIn(BaseModel):
    name: str = Field(max_length=40)
    surname: str = Field(max_length=40)
    email: str = Field(max_length=120)
    password: str = Field(max_length=5)


class UserOut(UserIn):
    id: int


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    goods_text = Column(String(225))
    price = Column(Float)

    orders = relationship("Order", back_populates="goods")


class GoodsIn(BaseModel):
    name: str = Field(max_length=40)
    goods_text: str = Field(max_length=225)
    price: float


class GoodsOut(GoodsIn):
    id: int


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goods_id = Column(Integer, ForeignKey("goods.id"))
    order_data = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(40))

    user = relationship("User", back_populates="orders")
    goods = relationship("Goods", back_populates="orders")


class OrderIn(BaseModel):
    user_id: int
    goods_id: int
    status: str = Field(max_length=40)


class OrderOut(OrderIn):
    id: int
    order_data: datetime.datetime


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = User(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserIn, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}


@app.get("/goods/", response_model=List[GoodsOut])
def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goods = db.query(Goods).offset(skip).limit(limit).all()
    return goods


@app.get("/goods/{goods_id}", response_model=GoodsOut)
def read_goods(goods_id: int, db: Session = Depends(get_db)):
    goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods


@app.post("/goods/", response_model=GoodsOut)
def create_goods(goods: GoodsIn, db: Session = Depends(get_db)):
    db_goods = Goods(name=goods.name, goods_text=goods.goods_text, price=goods.price)
    db.add(db_goods)
    db.commit()
    db.refresh(db_goods)
    return db_goods


@app.put("/goods/{goods_id}", response_model=GoodsOut)
def update_goods(goods_id: int, goods: GoodsIn, db: Session = Depends(get_db)):
    db_goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not db_goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    db_goods.name = goods.name
    db_goods.goods_text = goods.goods_text
    db_goods.price = goods.price
    db.commit()
    db.refresh(db_goods)
    return db_goods


@app.delete("/goods/{goods_id}")
def delete_goods(goods_id: int, db: Session = Depends(get_db)):
    db_goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not db_goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    db.delete(db_goods)
    db.commit()
    return {"message": "Goods deleted"}


@app.get("/orders/", response_model=List[OrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/orders/", response_model=OrderOut)
def create_order(order: OrderIn, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id, goods_id=order.goods_id, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderIn, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.user_id = order.user_id
    db_order.goods_id = order.goods_id
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted"}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": request})