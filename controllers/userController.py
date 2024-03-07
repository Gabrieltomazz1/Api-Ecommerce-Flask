from models.models import User
from flask_login import login_user, logout_user
from flask import jsonify


def handle_login(data):
    user = User.query.filter_by(user_name=data.get("user_name")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "User Logged successfully"})
    return jsonify({"message": "Unauthorized. Invalid Credential"}), 401


def handle_logout():
    logout_user()
    return jsonify({"message": "User Logout successfully"})
