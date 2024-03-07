from flask import Blueprint, request
from flask_login import login_required
from models.models import User
from controllers.userController import handle_login, handle_logout

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    return handle_login(data)


@user_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    return handle_logout()
