from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired


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
