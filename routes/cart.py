from flask import Blueprint, jsonify
from models.models import CartItem, User, Product
from flask_login import login_required, current_user
from config import db
from controllers.cartController import (
    handle_add_to_cart,
    handle_delete_from_cart,
    handle_view_cart,
    handle_checkout,
)

cart_blueprint = Blueprint("cart", __name__)


# Checkout
@cart_blueprint.route("/api/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    return handle_add_to_cart(product_id)


@cart_blueprint.route("/api/cart/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_from_cart(product_id):
    return handle_delete_from_cart(product_id)


@cart_blueprint.route("/api/cart", methods=["GET"])
@login_required
def view_cart():
    return handle_view_cart()


@cart_blueprint.route("/api/cart/checkout", methods=["POST"])
@login_required
def checkout():
    return handle_checkout()
