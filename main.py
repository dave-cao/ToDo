from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import CDN, Bootstrap
from sqlalchemy import desc

from forms import TodoForm
from models import Todo, db

app = Flask(__name__)

app.config["SECRET_KEY"] = "t432gwerg324qgwg24"
Bootstrap(app)

# Connect to cb
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

now = datetime.now().date()
yesterday = now - timedelta(days=3)


@app.route("/", methods=["GET", "POST"])
def home():
    todos = Todo.query.order_by(desc(Todo.date)).all()

    # separate todos into dates
    try:
        dates = [[todos[0]]]
    except IndexError:
        dates = []
    for i in range(len(todos) - 1):
        cur = todos[i]
        n = todos[i + 1]

        if n.date == cur.date:
            dates[-1].append(n)
        else:
            dates.append([n])

    print(dates)

    form = TodoForm(entrydate=now)
    if form.validate_on_submit():

        new_todo = Todo(
            task=form.task.data,
            date=form.entrydate.data,
            description=form.description.data,
        )
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("index.html", form=form, todos=dates)


@app.route("/delete<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/complete<int:todo_id>", methods=["GET", "PUT"])
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    todo.is_completed = not todo.is_completed
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
