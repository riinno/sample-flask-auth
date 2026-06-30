# by Riinno, 2026

# --------------------------------------------------------------------------
#Importação de dependencias e variaveis base

from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager

app = Flask(__name__)

# Criando uma chave secreta pro db
# Para estudo, está sendo definida com uma string
app.config['SECRET_KEY'] = "your_secret_key"

# Definindo o caminho para o SQLAlchemy se conetar ao db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

login_manager = LoginManager()

# Inicializando o app de db e login_manager (de database.py) com o 'app.py'
db.init_app(app)
login_manager.init_app(app)
# criar mais tarde o view login

# --------------------------------------------------------------------------
# Rota Login

@app.route("/login", methods=["POST"])
def login():
  data = request.get_json()
  username = data["username"]
  password = data["password"]

  # se alguma das infos for vazia, volta erro
  if not username or not password:
    return jsonify({"message": "Credenciais inválidas"}), 400
  
  # do contrario, deu certo

  # Login
  user_db = User.query.filter_by(username=username).first()
  
  if not user_db:
    return jsonify({"message": "Usuario incorreto ou inexistente"}), 400
  if not user_db.password == password:
    return jsonify({"message": "Senha incorreta"}), 400
  

  # do contrario, autenticou
  return jsonify({"message": "Autenticação realizada com sucesso"})

# --------------------------------------------------------------------------
# Rota Hello World (para testes iniciais)

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "hello world!"

# --------------------------------------------------------------------------
# Rota para inicialização manual

if __name__ == "__main__":
  app.run(debug=True)

# --------------------------------------------------------------------------