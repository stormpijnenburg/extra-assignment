from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

class Config:
    # Login credentials
    mysql_username = 'dbi502384'
    mysql_password = 'A2c37&ds$^7v'
    mysql_hostname = 'studmysql01.fhict.local'
    mysql_port = '3306'
    mysql_database_name = 'dbi502384'
    # Construct the MySQL database URI
    SQLALCHEMY_DATABASE_URI = f"mysql://{mysql_username}:{mysql_password}@{mysql_hostname}:{mysql_port}/{mysql_database_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TodoListApp:
    def __init__(self, Config):
        self.app = Flask(__name__, template_folder="./")
        self.app.config.from_object(Config)
        self.db = SQLAlchemy(self.app)

        # Define the Todo model
        class Todo(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            task = self.db.Column(self.db.String(100))
            done = self.db.Column(self.db.Boolean)

            def __init__(self, task, done=False):
                self.task = task
                self.done = done

        self.Todo = Todo

        # Routes
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/add", view_func=self.add, methods=["POST"])
        self.app.add_url_rule("/edit/<int:id>", view_func=self.edit, methods=["GET", "POST"])
        self.app.add_url_rule("/check/<int:id>", view_func=self.check)
        self.app.add_url_rule("/delete/<int:id>", view_func=self.delete)

    def index(self):
        todos = self.Todo.query.all()
        return render_template("index.html", todos=todos)

    def add(self):
        todo = request.form['todo']
        new_todo = self.Todo(todo)
        self.db.session.add(new_todo)
        self.db.session.commit()
        return redirect(url_for("index"))

    def edit(self, id):
        todo = self.Todo.query.get(id)
        if request.method == "POST":
            new_task = request.form["todo"]
            todo.task = new_task
            self.db.session.commit()
            return redirect(url_for("index"))
        else:
            return render_template("edit.html", todo=todo)

    def check(self, id):
        todo = self.Todo.query.get(id)
        todo.done = not todo.done
        self.db.session.commit()
        return redirect(url_for("index"))

    def delete(self, id):
        todo = self.Todo.query.get(id)
        self.db.session.delete(todo)
        self.db.session.commit()
        return redirect(url_for("index"))

    def initialize_database(self):
        with self.app.app_context():
            self.db.create_all()

    def run(self):
        self.initialize_database()
        self.app.run(debug=True)

if __name__ == "__main__":
    todo_list_app = TodoListApp(Config)
    todo_list_app.run()
