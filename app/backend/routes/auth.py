from flask import Blueprint, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # JWT is stateless. Client-side should delete the token.
    # Server-side token revocation can be added with Redis if needed.
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    return AuthController.get_profile()

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    return AuthController.update_profile()