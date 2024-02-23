from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Commun flask inicializacion
app = Flask(__name__)

# inicialização do banco de dados usando SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
db = SQLAlchemy(app)
# É necessario utilizar estes comandos para iniciar este modelo de banco de dados
# flash shell
# db.create_all


# Modelagem do banco de dados
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# define a rota raiz e a função que sera executada ao requisitar
@app.route("/")
def hello_world():
    return "Hello world"


@app.route("/api/products/add", methods=["POST"])
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


# limita a criação de servidores, Inicializa o servidor apenas quando acontecer a ocorrencia de "__main__"
if __name__ == "__main__":
    app.run(debug=True)


# time 01;06;42
