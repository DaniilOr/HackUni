from app import app
from flask import render_template, jsonify
from flask import request
from flask import make_response
from app.models import db, User
from flask_cors import CORS, cross_origin
import json
from useful_tools import *

@app.route('/')
@app.route('/index')
@cross_origin()
def index():
    return make_response(jsonify({'Result': 'Connected'}), 200)


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    my_json = request.get_json()
    username = my_json.get('username')
    password = my_json.get('password')
    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.check_password(password):
        return make_response(jsonify({'Result': 'Failed, password missmatch'}), 404)
    else:
        return make_response(jsonify({'Result': 'Logged in'}), 200)


@app.route('/get_users', methods=['GET', 'POST'])
@cross_origin()
def get_users():
    my_json = request.get_json()
    roles = my_json.get('roles')
    needed_people = db.query(User).filter(User.role in roles).all()
    needed_people.sort(key=lambda x: (x.rating, x.distance, x.priority))
    return make_response(jsonify(needed_people), 200)


@app.route('/change_priority', methods=['GET', 'POST'])
@cross_origin()
def change_priority():
    my_json = request.get_json()
    id = my_json.get('id')
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        return make_response(jsonify({'Response':'Not found'}), 404)
    user.priority = not user.priority
    db.commit()


@app.route('/get_all', methods=['GET', 'POST'])
@cross_origin()
def get_all():
    people = db.query(User).all()
    return make_response(jsonify(people), 200)


@app.route('/register', methods=['GET', 'POST'])
@cross_origin()
def register():
    my_json = request.get_json()
    username = my_json.get('username')
    password = my_json.get('password')
    role = my_json.get('role')
    distance = my_json.get('distance')
    description = my_json.get('description')
    price = my_json.get('price')
    email = my_json.get('email')
    if not uname_check(username) is None or not email_check(email) is None:
        return make_response(jsonify({'Result':'Failed, chnge username or email'}), 200)
    else:
        user = User(username=username, role=role, price=price, description=description,
                    distance=distance, email=email)
        user.set_password(password)
        db.add(user)
        db.commit()
        return make_response(jsonify({'Result':'Registered'}), 200)


@app.route('/get_specific_role', methods=['GET', 'POST'])
@cross_origin()
def get_specific_role():
    my_json = request.get_json()
    role = my_json.get('role')
    users = db.query(User).filter(User.role == role).all()
    make_response(jsonify(users), 200)
