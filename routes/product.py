from flask import Blueprint, request
from flask_login import login_required
from models.models import Product
from controllers.productController import (
    handle_product_add,
    handle_delete_product,
    handle_product_detail,
    handle_update_product,
    handle_all_products,
)


product_blueprint = Blueprint("product", __name__)


@product_blueprint.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
    return handle_product_add(data)


# Para receber parametros é necessario utilizar <int:product_id> junto a rota
@product_blueprint.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    return handle_delete_product(product_id)


@product_blueprint.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
    return handle_product_detail(product_id)


@product_blueprint.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    return handle_update_product(product_id)


@product_blueprint.route("/api/products", methods=["GET"])
def get_products():
    return handle_all_products()
