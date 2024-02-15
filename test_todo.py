import pytest
from app import TodoListApp

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    todo_list_app = TodoListApp(Config)
    return todo_list_app.app

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_todo_item(client):
    response = client.post('/add', data={'todo': 'Test todo item'})
    assert response.status_code == 302  # Check if redirecting after adding
    assert b'Test todo item' in response.data  # Check if the added item is in the response

def test_check_todo_item(client):
    # Add a todo item first
    response = client.post('/add', data={'todo': 'Test todo item to check'})
    assert response.status_code == 302

    # Get the id of the added item
    todo_id = int(response.headers['Location'].split('/')[-1])

    # Check the todo item
    response = client.get(f'/check/{todo_id}')
    assert response.status_code == 302  # Check if redirecting after checking

def test_delete_todo_item(client):
    # Add a todo item first
    response = client.post('/add', data={'todo': 'Test todo item to delete'})
    assert response.status_code == 302

    # Get the id of the added item
    todo_id = int(response.headers['Location'].split('/')[-1])

    # Delete the todo item
    response = client.get(f'/delete/{todo_id}')
    assert response.status_code == 302  # Check if redirecting after deleting
