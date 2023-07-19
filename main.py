"""

Portfolio: ToDo_List Project
#100DaysOfCode with Python
Day: 87
Date: 2023-07-15
Author: MC

"""

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


from Forms.Forms import *

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


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
    return render_template("home.html",
                           current_user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, pleas try again. ")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, pleas try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash(f"user: {user.name}")
            return redirect(url_for('home'))

    return render_template('login.html',
                           form=form,
                           current_user=current_user)


@app.route('/show_task')
def show_task():
    return render_template('show_task.html')


@app.route('/tasks')
def tasks():

    all_tasks = ToDoList.query.all()

    all_status = Status.query.all()

    return render_template('tasks.html',
                           all_tasks=all_tasks,
                           all_status=all_status,
                           current_user=current_user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if request.method == 'POST':

            # check if user in db
            if Users.query.filter_by(email=request.form.get('email')).first():
                flash("You've already singed up with that email, log in instead.")
                return redirect(url_for('login'))

            # create new user
            hash_pdw = request.form.get('password')
            hash_pdw = generate_password_hash(hash_pdw,
                                              method='pbkdf2:sha256',
                                              salt_length=8)

            new_user = Users(
                email=request.form.get('email'),
                password=hash_pdw,
                name=request.form.get('name')
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('home'))

    return render_template('register.html',
                           form=form,
                           current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html',
                           current_user=current_user)


@app.route('/contact')
def contact():
    return render_template('contact.html',
                           current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True)

