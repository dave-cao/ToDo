from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, EmailField, PasswordField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired, Email


class TodoForm(FlaskForm):
    task = StringField(
        label="Task",
        validators=[DataRequired()],
        render_kw={"autofocus": True},
    )
    is_completed = BooleanField(label="Is this task completed?")
    entrydate = DateField(label="entrydate")
    description = StringField(label="description")
    submit = SubmitField(label="Add Item")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
