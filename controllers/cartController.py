from config import db
from models.models import CartItem, User, Product
from flask_login import current_user
from flask import jsonify


def handle_add_to_cart(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(int(product_id))
    if user and product:

        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()

        return jsonify({"Message": "Added to the cart successfully"})
    return jsonify({"Message": "Failed to add the cart"}), 400


def handle_delete_from_cart(product_id):
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"Message": "Product removed successfully"})
    return jsonify({"Message:": "Product not found"}), 400


def handle_view_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        cart_content.append(
            {
                "id": cart_item.id,
                "user_id": cart_item.user_id,
                "product_id": cart_item.product_id,
                "product_name": product.name,
                "product_price": product.price,
            }
        )
    return jsonify(cart_content)


def handle_checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"Message": "Checout successfully. Cart has been cleared"})
