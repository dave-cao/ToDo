import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
db = SQLAlchemy(app)

now = datetime.now()


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=False, nullable=False)
    date = db.Column(db.DateTime(now))
    is_completed = db.Column(db.Boolean(False))
    description = db.Column(db.String(250))
    date_created = db.Column(db.DateTime(now))


with app.app_context():
    db.create_all()
