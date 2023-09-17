import jwt
import datetime
payload = {'sub':'test','user_id': 1, 'user_type': 'teacher'}
#payload = {'user_id': 123, 'user_type': 'admin'}
payload = {}

# Set the JWT secret key
JWT_SECRET_KEY = 'your-secret-key'

# Set the JWT algorithm
JWT_ALGORITHM = 'HS256'

# Set the JWT expiry time
JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)

# Define the payload for the JWT
payload = {
    'sub': 1,
    'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA,
    'user_id': 1,
    'user_type': 'student'
}

# Generate the JWT token
jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# Print the JWT token
print(jwt_token)