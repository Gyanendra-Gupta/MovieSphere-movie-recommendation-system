from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def protected_route():
    """
    Optional custom decorator if we want to add extra logic 
    beyond standard @jwt_required().
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({"message": "User no longer exists"}), 401
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({"message": "Authentication required"}), 401
        return decorated_function
    return decorator