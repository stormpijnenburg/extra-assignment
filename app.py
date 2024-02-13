from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="./")

# Login credentials
mysql_username = 'dbi502384'
mysql_password = 'A2c37&ds$^7v'
mysql_hostname = 'studmysql01.fhict.local'
mysql_port = '3306'
mysql_database_name = 'dbi502384'

# Construct the MySQL database URI
mysql_uri = f"mysql://{mysql_username}:{mysql_password}@{mysql_hostname}:{mysql_port}/{mysql_database_name}"

# Set the SQLAlchemy configuration to use MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __init__(self, task, done=False):
        self.task = task
        self.done = done

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo = request.form['todo']
    new_todo = Todo(todo)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get(id)
    if request.method == "POST":
        new_task = request.form["todo"]
        todo.task = new_task
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo)

@app.route("/check/<int:id>")
def check(id):
    todo = Todo.query.get(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
