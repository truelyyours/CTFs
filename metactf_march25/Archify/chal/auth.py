import jwt
import datetime
from flask import redirect, url_for, current_app, request
from functools import wraps

# Generate JWT token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'role': 'user',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to protect routes
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')  # Get token from cookies
        if not token:
            # Redirect to login if no token is found
            return redirect(url_for('login'))

        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))  # Redirect if token has expired
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))  # Redirect if token is invalid

        # Attach user_id to the request context
        request.user_id = decoded['user_id']
        return f(*args, **kwargs)
    return decorated_function

# {
#   "user_id": "admin",
#   "role": "user",
#   "exp": 1743121447
# }

# {
#   "user_id": "admin",
#   "role": "user",
#   "exp": 1743121447
# }