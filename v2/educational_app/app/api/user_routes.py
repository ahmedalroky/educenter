from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User  # Adjust the import path as needed
from ..services.authentication import AuthenticationService, token_required  # Adjust the import path

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'message': 'Missing information'}), 400

    if User.find_by_username(username):
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)

    try:
        user.save_to_db()  # Assume your User model has a method for saving to the database
        return jsonify({'message': 'User created successfully'}), 201
    except:
        return jsonify({'message': 'Failed to create user'}), 500

@user_bp.route('/users/login', methods=['POST'])
def login():
    data = request.json
    user = User.find_by_username(data.get('username'))

    if user and check_password_hash(user.password, data.get('password')):
        token = AuthenticationService.encode_token(user.id)  # Adjust method name as necessary
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {'username': user.username, 'email': user.email}  # Customize based on your User model
    return jsonify(user_data), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    
    user.save_to_db()
    return jsonify({'message': 'User updated successfully'}), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.delete_from_db()
    return jsonify({'message': 'User deleted successfully'}), 200
