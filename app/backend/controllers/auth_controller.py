from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required
)
from models import db, User, Genre
import re

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        
        # Validation
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        preferred_genres = data.get('genres', []) # List of genre names

        if not all([name, email, password, confirm_password]):
            return jsonify({"message": "All fields are required"}), 400

        if password != confirm_password:
            return jsonify({"message": "Passwords do not match"}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"message": "Invalid email format"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered"}), 409

        # Create User
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        # Handle Genres
        if preferred_genres:
            genres = Genre.query.filter(Genre.name.in_(preferred_genres)).all()
            new_user.preferred_genres = genres

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "profile_image": user.profile_image,
                    "genres": [g.name for g in user.preferred_genres]
                }
            }), 200

        return jsonify({"message": "Invalid email or password"}), 401

    @staticmethod
    @jwt_required()
    def get_profile():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "profile_image": user.profile_image,
            "genres": [g.name for g in user.preferred_genres],
            "created_at": user.created_at.isoformat()
        }), 200

    @staticmethod
    @jwt_required()
    def update_profile():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if 'name' in data:
            user.name = data['name']
        if 'profile_image' in data:
            user.profile_image = data['profile_image']
        if 'genres' in data:
            genres = Genre.query.filter(Genre.name.in_(data['genres'])).all()
            user.preferred_genres = genres
        if 'password' in data and data['password']:
            user.set_password(data['password'])

        try:
            db.session.commit()
            return jsonify({"message": "Profile updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update profile"}), 500