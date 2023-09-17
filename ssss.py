from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Mock user database
users = {
    'john': 'password123',
    'jane': 'password456'
}

# Authentication endpoint
@app.route('/auth', methods=['POST'])
def auth():
    # Get username and password from request body
    auth_data = request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    # Check if username and password match a user in the database
    if username in users and users[username] == password:
        # Create JWT token with a 30 minute expiration
        payload = {'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Protected endpoint that requires authentication
@app.route('/protected', methods=['GET'])
def protected():
    # Get JWT token from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(' ')[1]
    else:
        return jsonify({'error': 'No token provided'}), 401

    # Verify JWT token
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload.get('username')
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    # Return protected data
    return jsonify({'message': f'Hello, {username}!'})

if __name__ == '__main__':
    app.run(debug=True)
