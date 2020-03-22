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
    password = my_json.get('password')
    email = my_json.get('email')
    user = db.session.query(User).filter(User.email == email).first()

    if user is None or not user.check_password(password):
        return make_response(jsonify({'Result': 'Failed, password missmatch'}), 404)
    else:
        return make_response(jsonify({'Result': 'Logged in'}), 200)


@app.route('/get_users', methods=['GET', 'POST'])
@cross_origin()
def get_users():
    my_json = request.get_json()
    roles = my_json.get('roles')
    needed_people = db.session.query(User).filter(User.role in roles).all()
    result = []
    for person in needed_people:
        p = {}
        p['username'] = person.username
        p['id'] = person.id
        p['email'] = person.email
        p['password'] = person.password_hash
        p['distance'] = person.distance
        p['description'] = person.description
        p['priority'] = person.priority
        p['price'] = person.price
        p['role'] = person.role
        p['rating'] = person.rating
        p['avatar'] = person.avatar
        result.append(p)
    result.sort(key=lambda x: (x['rating'], x['distance'], x['priority']), reverse=True)
    return make_response(jsonify(result), 200)


@app.route('/change_priority', methods=['GET', 'POST'])
@cross_origin()
def change_priority():
    my_json = request.get_json()
    id = my_json.get('id')
    user = db.session.query(User).filter(User.id == id).first()
    if user is None:
        return make_response(jsonify({'Response':'Not found'}), 404)
    user.priority = not user.priority
    db.session.commit()
    return make_response(jsonify({'Result':'Changed'}), 200)


@app.route('/get_all', methods=['GET', 'POST'])
@cross_origin()
def get_all():
    people = db.session.query(User).all()
    result = []
    for person in people:
        p = {}
        p['username'] = person.username
        p['id'] = person.id
        p['email'] = person.email
        p['password'] = person.password_hash
        p['distance'] = person.distance
        p['description'] = person.description
        p['priority'] = person.priority
        p['price'] = person.price
        p['role'] = person.role
        p['avatar'] = person.avatar
        result.append(p)
    return make_response(jsonify(result), 200)


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
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'Result':'Registered'}), 200)


@app.route('/get_specific_role', methods=['GET', 'POST'])
@cross_origin()
def get_specific_role():
    my_json = request.get_json()
    role = my_json.get('role')
    users = db.session.query(User).filter(User.role == role).all()
    result = []
    for person in users:
        p = {}
        p['username'] = person.username
        p['id'] = person.id
        p['email'] = person.email
        p['password'] = person.password_hash
        p['distance'] = person.distance
        p['description'] = person.description
        p['priority'] = person.priority
        p['price'] = person.price
        p['role'] = person.role
        p['rating'] = person.rating
        p['avatar'] = person.avatar
        result.append(p)
    result.sort(key=lambda x: (x['rating'], x['distance'], x['priority']), reverse=True)
    return make_response(jsonify(result), 200)


@app.route('/invite', methods=['GET', 'POST'])
@cross_origin()
def invite():
    my_json = request.get_json()
    user_id = my_json.get('id')
    description = my_json.get('description')
    description = delete_numbers(delete_emails(description))
    selected_user = db.session.query(User).filter(User.id == user_id).first()
    if not selected_user is None:
        send_mail(selected_user.email, description)
        return make_response(jsonify({'Result': 'Invitation is sent'}), 200)
    else:
        return make_response(jsonify({'Result':'User not found'}), 404)


