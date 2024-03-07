from models.models import Product
from config import db
from flask import jsonify, request


def handle_product_add(data):
    if "name" in data and "price" in data:
        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400


def handle_delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404


def handle_product_detail(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
            }
        )
    return jsonify({"message": "Product not found"}), 404


def handle_update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    data = request.json
    if "name" in data:
        product.name = data["name"]
    if "price" in data:
        product.price = data["price"]
    if "description" in data:
        product.description = data["description"]
    db.session.commit()
    return jsonify({"message": "Product update succesfully"})


def handle_all_products():
    products = Product.query.all()
    product_list = []

    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }
        product_list.append(product_data)

    return jsonify(product_list)
