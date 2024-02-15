import pytest
from flask_sqlalchemy import SQLAlchemy
from app import TodoListApp

class TestConfig:
    # Construct the MySQL database URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def client():
    app = TodoListApp(TestConfig)
    app.initialize_database()
    yield app

def test_add_todo(client):
    client = client.app.test_client
    todos = client.Todo.query.all()
    previousCount = len(todos)

    response = client.post('/add', data={'todo': 'Test Todo'})

    todos = client.Todo.query.all()

    assert response.status_code == 302  # Check if redirected
    assert len(todos) == previousCount + 1
    assert todos[-1].task == 'Test Todo'

def test_check_todo(client):
    todo = client.Todo(task='Test Todo')
    client.db.session.add(todo)
    client.db.session.commit()

    response = client.get(f'/check/{todo.id}')
    assert response.status_code == 302  # Check if redirected
    assert client.Todo.query.get(todo.id).done

def test_delete_todo(client):
    todo = client.Todo(task='Test Todo')
    client.db.session.add(todo)
    client.db.session.commit()

    response = client.get(f'/delete/{todo.id}')
    assert response.status_code == 302  # Check if redirected
    assert client.Todo.query.get(todo.id) is None
