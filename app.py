from flask_login import LoginManager
from config import app
from routes.cart import cart_blueprint
from routes.user import user_blueprint
from routes.product import product_blueprint


# Inicialização do LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Autenticação
@login_manager.user_loader
def load_user(user_id):
    from models.models import User  # Certifique-se de importar corretamente

    return User.query.get(int(user_id))


# Registro das blueprints
app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(cart_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
