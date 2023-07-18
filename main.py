"""

Portfolio: ToDo_List Project
#100DaysOfCode with Python
Day: 87
Date: 2023-07-15
Author: MC

"""

from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1000))


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    id_status = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.String(12))
    end_date = db.Column(db.String(12))


class User_Task(db.Model):
    __tablename__ = 'user_tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)


@app.route("/")
def home():
    # return render_template("index.html")
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

