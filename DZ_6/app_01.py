import datetime
from typing import List
import databases
import pandas as pd
import sqlalchemy
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from sqlalchemy import DATE, Float



DATABASE_URL = "sqlite:///shop.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("goods_name", sqlalchemy.String(40)),
    sqlalchemy.Column("goods_text", sqlalchemy.String(120)),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("goods_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("goods.id")),
    sqlalchemy.Column("order_data", sqlalchemy.DATE),
    sqlalchemy.Column("status", sqlalchemy.String(40))
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(40)),
    sqlalchemy.Column("surname", sqlalchemy.String(40)),
    sqlalchemy.Column("email", sqlalchemy.String(120)),
    sqlalchemy.Column("password", sqlalchemy.Integer),

)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="./DZ_6/templates")

class User(BaseModel):
    id: int
    name: str = Field(max_length=40)
    surname: str = Field(max_length=40)
    email: str = Field(max_length=120)
    password: str = Field(max_length=5)

class UserIn(BaseModel):
    name: str = Field(max_length=40)
    surname: str = Field(max_length=40)
    email: str = Field(max_length=120)
    password: str = Field(max_length=5)



class Goods(BaseModel):
    id: int
    name: str = Field(max_length=40)
    goods_text: str = Field(max_length=225)
    price: Float = Field(max_length=40)


class GoodsIn(BaseModel):
    name: str = Field(max_length=40)
    goods_text: str = Field(max_length=225)
    price: Float = Field(max_length=40)



class Order(BaseModel):
    id: int
    user_id: int
    goods_id: int
    order_data: datetime.datetime
    status: str = Field(max_length=40)

class OrderIn(BaseModel):
    user_id: int
    goods_id: int
    order_data: datetime.datetime
    status: str = Field(max_length=40)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.model_dump(), "id": record_id}


@app.get("/users/", response_model=List[User])
async def read_user():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    print(await database.execute(query))
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


#
# # Маршруты для товаров
# @app.post("/goods/", response_model=Goods)
# async def create_goods(goods: GoodsCreate):
#     query = goods.insert().values(
#         goods_name=goods.goods_name,
#         goods_text=goods.goods_text,
#         price=goods.price
#     )
#     last_record_id = await database.execute(query)
#     return {**goods.dict(), "id": last_record_id}
#
# @app.get("/goods/{goods_id}", response_model=Goods)
# async def read_goods(goods_id: int):
#     query = goods.select().where(goods.c.id == goods_id)
#     goods_record = await database.fetch_one(query)
#     if goods_record is None:
#         raise HTTPException(status_code=404, detail="Goods not found")
#     return goods_record
#
# @app.put("/goods/{goods_id}", response_model=Goods)
# async def update_goods(goods_id: int, updated_goods: GoodsCreate):
#     query = goods.update().where(goods.c.id == goods_id).values(
#         goods_name=updated_goods.goods_name,
#         goods_text=updated_goods.goods_text,
#         price=updated_goods.price
#     )
#     await database.execute(query)
#     return {**updated_goods.dict(), "id": goods_id}
#
# @app.delete("/goods/{goods_id}")
# async def delete_goods(goods_id: int):
#     query = goods.delete().where(goods.c.id == goods_id)
#     await database.execute(query)
#     return {"message": "Goods deleted successfully"}
#
# # Маршруты для заказов
# @app.post("/orders/", response_model=Orders)
# async def create_orders(orders: OrdersCreate):
#     query = orders.insert().values(
#         user_id=orders.user_id,
#         goods_id=orders.goods_id,
#         status=orders.status
#     )
#     last_record_id = await database.execute(query)
#     return {**orders.dict(), "id": last_record_id}
#
# @app.get("/orders/{orders_id}", response_model=Orders)
# async def read_orders(orders_id: int):
#     query = orders.select().where(orders.c.id == orders_id)
#     orders_record = await database.fetch_one(query)
#     if orders_record is None:
#         raise HTTPException(status_code=404, detail="Orders not found")
#     return orders_record
#
# @app.put("/orders/{orders_id}", response_model=Orders)
# async def update_orders(orders_id: int, updated_orders: OrdersCreate):
#     query = orders.update().where(orders.c.id == orders_id).values(
#         user_id=updated_orders.user_id,
#         goods_id=updated_orders.goods_id,
#         status=updated_orders.status
#     )
#     await database.execute(query)
#     return {**updated_orders.dict(), "id": orders_id}
#
# @app.delete("/orders/{orders_id}")
# async def delete_orders(orders_id: int):
#     query = orders.delete().where(orders.c.id == orders_id)
#     await database.execute(query)
#     return {"message": "Orders deleted successfully"}


#

#----------------------------------------------------------
#-----------------------------------------------------------
# @app.post("/goods/", response_model=DZ_6_1.goods_class.Goods)
# async def create_user(good: DZ_6_1.goods_class.GoodsIn):
#     query = goods.insert().values(**good.model_dump())
#     record_id = await database.execute(query)
#     return {**good.model_dump(), "id": record_id}
#
#
# @app.get("/goods/", response_model=List[DZ_6_1.goods_class.Goods])
# async def read_user():
#     query = goods.select()
#     return await database.fetch_all(query)
#
#
# @app.get("/goods/{goods_id}", response_model=DZ_6_1.goods_class.Goods)
# async def read_user(goods_id: int):
#     query = goods.select().where(users.c.id == goods_id)
#     return await database.fetch_one(query)
#
#
# @app.put("/goods/{goods_id}", response_model=DZ_6_1.goods_class.Goods)
# async def update_user(goods_id: int, new_good: DZ_6_1.goods_class.GoodsIn):
#     query = goods.update().where(goods.c.id == goods_id).values(**new_good.model_dump())
#     print(await database.execute(query))
#     return {**new_good.model_dump(), "id": goods_id}
#
#
# @app.delete("/goods/goods_id}")
# async def delete_user(goods_id: int):
#     query = users.delete().where(users.c.id == goods_id)
#     await database.execute(query)
#     return {'message': 'User deleted'}
#
#
# ##------------------------------------------
#
# @app.post("/orders/", response_model=DZ_6_1.orders_class.Order)
# async def create_user(order: DZ_6_1.orders_class.OrderIn):
#     query = orders.insert().values(**order.model_dump())
#     record_id = await database.execute(query)
#     return {**order.model_dump(), "id": record_id}
#
#
# @app.get("/orders/", response_model=List[DZ_6_1.orders_class.Order])
# async def read_user():
#     query = orders.select()
#     return await database.fetch_all(query)
#
#
# @app.get("/orders/{orders_id}", response_model=DZ_6_1.orders_class.Order)
# async def read_user(orders_id: int):
#     query = orders.select().where(users.c.id == orders_id)
#     return await database.fetch_one(query)
#
#
# @app.put("/orders/{orders_id}", response_model=DZ_6_1.orders_class.Order)
# async def update_user(orders_id: int, new_order: DZ_6_1.orders_class.OrderIn):
#     query = orders.update().where(orders.c.id == orders_id).values(**new_order.model_dump())
#     print(await database.execute(query))
#     return {**new_order.model_dump(), "id": orders_id}
#
#
# @app.delete("/orders/orders_id}")
# async def delete_user(orders_id: int):
#     query = users.delete().where(users.c.id == orders_id)
#     await database.execute(query)
#     return {'message': 'User deleted'}