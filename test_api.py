import requests
from server import db


def test_main_page_get():
    response = requests.get(url='http://127.0.0.1:8000/api/v1/main_page')

    assert response is not None
    assert int(response.status_code) == 200
    assert response.json() == {"greeting": "Welcome to Paul's Pizza!"}


def test_all_pizzas_get():
    response = requests.get(url='http://127.0.0.1:8000/api/v1/pizza_page')

    assert response is not None
    assert int(response.status_code) == 200
    assert response.json() == {"pizzas": db}


def test_one_pizzas_get():
    response = requests.get(url='http://127.0.0.1:8000/api/v1/pizza_page/1')

    assert response is not None
    assert int(response.status_code) == 200
    print(response.json())
    assert response.json() == {"pizza": db[1]}


def test_one_pizzas_post():
    data = {
            'name': 'New Pizza',
            'toppings': ['Mozzarella cheese', 'Tomatoes', 'Basil']
        }
    last_id = db[-1]['id']
    response = requests.post(
        url='http://127.0.0.1:8000/api/v1/pizza_page',
        json=data,
    )

    data['id'] = response.json()['id']
    assert response is not None
    assert int(response.status_code) == 200
    assert data == response.json()
    assert response.json()['id'] != last_id


def test_one_pizzas_delete():
    response = requests.delete(url='http://127.0.0.1:8000/api/v1/pizza_page/1')

    pizza = {
        'id': 1,
        'name': 'Chicago/Deep-Dish Pizza',
        'toppings': ['Cheese', 'Tomatoes', 'pepperoni', 'Onions', 'Mushrooms']
    }

    assert response is not None
    assert int(response.status_code) == 200
    assert pizza not in response.json()['data']


def test_one_pizzas_put():
    data = {
            'name': 'New Pizza',
            # 'toppings': ['Mozzarella cheese', 'Tomatoes', 'Basil']
        }
    response = requests.put(
        url='http://127.0.0.1:8000/api/v1/pizza_page/1',
        json=data,
    )

    assert response is not None
    assert int(response.status_code) == 200
    assert data['name'] == response.json()['name']
    assert db[1]['toppings'] == response.json()['toppings']