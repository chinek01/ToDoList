"""


Forms for ToDo_list project

#100DaysOfCode with Python
Day: 87
Date: 2023-07-16
Author: MC

"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm
class RegisterForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    submit = SubmitField("Create user")


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Login")


class NewTaskForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    start_date = DateField("Start date: ", validators=[DataRequired()])
    end_date = DateField("End date:", validators=[DataRequired()])
    submit = SubmitField("Submit")
