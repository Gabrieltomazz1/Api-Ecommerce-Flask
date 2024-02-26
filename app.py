from crypt import methods
from flask import Flask, request, jsonify
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy

# Commun flask inicializacion
app = Flask(__name__)

# Gerencia os usuarios

login_manager = LoginManager()

# inicialização do banco de dados usando SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SECRET_KEY"] = "mykey"
db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = "login"
# É necessario utilizar estes comandos para iniciar este modelo de banco de dados
# flash shell
# db.create_all


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)


# Modelagem do banco de dados
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
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


# Para receber parametros é necessario utilizar <int:product_id> junto a rota
@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    # Recuperar o produto da base de dados
    # Validação
    # Apagar caso exista
    # Retonar 404 not found
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
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


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
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


@app.route("/api/products", methods=["GET"])
def get_products():
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


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(user_name=data.get("user_name")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "User Logged successfully"})
    return jsonify({"message": "Unauthorized. Invalid Credential"}), 401

@app.route("/logout", methods= ["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User Logout successfully"})
    



# limita a criação de servidores, Inicializa o servidor apenas quando acontecer a ocorrencia de "__main__"
if __name__ == "__main__":
    app.run(debug=True)


# time 03:0:0
