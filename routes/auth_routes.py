from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from utils.db_config import db

auth_bp = Blueprint('auth', __name__)

SECRET = current_app.config.get('SECRET_KEY') if False else 'replace-with-secure-key'  # replaced at runtime

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    if not email or not password:
        return jsonify({'error':'email and password required'}), 400
    users = db.collection('users').where('email','==',email).get()
    if users:
        return jsonify({'error':'user exists'}), 400
    user_doc = {
        'email': email,
        'password': generate_password_hash(password),
        'role': role,
        'created_at': datetime.datetime.utcnow()
    }
    db.collection('users').add(user_doc)
    return jsonify({'message':'user created'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error':'email and password required'}), 400
    users = db.collection('users').where('email','==',email).get()
    if not users:
        return jsonify({'error':'invalid credentials'}), 401
    user = users[0].to_dict()
    if not check_password_hash(user['password'], password):
        return jsonify({'error':'invalid credentials'}), 401
    payload = {
        'email': email,
        'role': user.get('role','student'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200
