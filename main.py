from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import CDN, Bootstrap
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegisterForm, TodoForm
from models import Todo, User, db

app = Flask(__name__)

app.config["SECRET_KEY"] = "t432gwerg324qgwg24"
Bootstrap(app)

# Connect to cb
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Flask Login Functions
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/", methods=["GET", "POST"])
def home():
    now = datetime.now()
    todos = Todo.query.order_by((Todo.date)).all()
    if current_user.is_authenticated:
        todos = [todo for todo in todos if todo.user == current_user]
    else:
        todos = [todo for todo in todos if todo.user == None]

    # separate todos into dates
    # THIS CAN GO INTO ITS OWN FUNCTION
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

    # CALCULATE HOW MANY DAYS AGO EACH WAS?
    for date in dates:
        actual_date = date[-1].date

    form = TodoForm(entrydate=now)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_todo = Todo(
                task=form.task.data,
                date=form.entrydate.data,
                description=form.description.data,
                date_created=now,
                user=current_user,
                user_id=current_user.id,
            )
        else:
            new_todo = Todo(
                task=form.task.data,
                date=form.entrydate.data,
                description=form.description.data,
                date_created=now,
            )

        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("index.html", form=form, todos=dates, now=now)


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


# ================= LOGIN / REGISTER ============================== #
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists! Please login instead.")
            return redirect(url_for("login"))

        # If user doesn't exist then create user
        password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(email=email, password=password, name=form.name.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        # if user exists, than check hashed password
        if not user:
            flash("This email doesn't exist in our database!")
            return render_template("login.html", form=form)

        # check hashed password
        if check_password_hash(pwhash=user.password, password=form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            # password is incorrect
            flash("Incorrect password, try again!")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
