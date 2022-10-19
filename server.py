import uuid
import json
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List

app = FastAPI()

API_PATH = '/api/v1/'

db = [
    {
        'id': 0,
        'name': 'Neapolitan Pizza',
        'toppings': ['Mozzarella cheese', 'Tomatoes', 'Basil']
    },
    {
        'id': 1,
        'name': 'Chicago/Deep-Dish Pizza',
        'toppings': ['Cheese', 'Tomatoes', 'pepperoni', 'Onions', 'Mushrooms']
    },
]


@app.get(API_PATH + 'main_page')
async def index():
    return {"greeting": "Welcome to Paul's Pizza!"}


@app.get(API_PATH + 'pizza_page')
async def all_pizzas():
    return {"pizzas": db}


@app.get(API_PATH + 'pizza_page/{pizza_id:int}')
async def get_one_pizzas(pizza_id):
    for element in db:
        if element['id'] == pizza_id:
            return {'pizza': element}
    return {"pizza": None}


class Pizza(BaseModel):
    name: str
    toppings: List[str]


@app.post(API_PATH + 'pizza_page')
async def post_one_pizzas(pizza: Pizza):
    new_pizza = pizza.dict()
    new_pizza['id'] = db[-1]['id'] + 1
    db.append(new_pizza)
    return new_pizza


@app.delete(API_PATH + 'pizza_page/{pizza_id:int}')
async def delete_one_pizzas(pizza_id):
    for element in db:
        if element['id'] == pizza_id:
            db.remove(element)
    return {"data": db}


class PizzaPut(BaseModel):
    name: str = None
    toppings: List[str] = None


@app.put(API_PATH + 'pizza_page/{pizza_id:int}')
async def put_one_pizzas(pizza_id, pizza: PizzaPut):
    for element in db:
        if element['id'] == pizza_id:
            new_pizza = pizza.dict()
            if new_pizza['name'] is not None:
                element['name'] = new_pizza['name']
            if new_pizza['toppings'] is not None:
                element['toppings'] = new_pizza['toppings']
            return element