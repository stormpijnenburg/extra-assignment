import pytest
from app import TodoListApp

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    return TodoListApp(Config)

def test_add_todo_item(app):
    with app.app.test_client() as client:
        # Send a POST request to add a new todo item
        response = client.post("/add", data={"todo": "Test todo item"})
        assert response.status_code == 302  # Check if redirected after adding
        # Check if the added todo item is present in the index page
        response = client.get("/")
        assert b"Test todo item" in response.data


def test_remove_todo_item(app):
    with app.app.test_client() as client:
        # Send a POST request to add a new todo item
        client.post("/add", data={"todo": "Test todo item to remove"})
        # Get the id of the added todo item
        todo_id = app.Todo.query.filter_by(task="Test todo item to remove").first().id
        # Send a GET request to delete the added todo item
        response = client.get(f"/delete/{todo_id}")
        assert response.status_code == 302  # Check if redirected after deleting
        # Check if the deleted todo item is not present in the index page
        response = client.get("/")
        assert b"Test todo item to remove" not in response.data


def test_edit_todo_item(app):
    with app.app.test_client() as client:
        # Send a POST request to add a new todo item
        client.post("/add", data={"todo": "Test todo item to edit"})
        # Get the id of the added todo item
        todo_id = app.Todo.query.filter_by(task="Test todo item to edit").first().id
        # Send a POST request to edit the added todo item
        response = client.post(f"/edit/{todo_id}", data={"todo": "Edited todo item"})
        assert response.status_code == 302  # Check if redirected after editing
        # Check if the edited todo item is present in the index page
        response = client.get("/")
        assert b"Edited todo item" in response.data
