# Code by Riinno, 2026

# --------------------------------------------------------------------------------------------
#Importação de dependencias e variaveis base

from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

# Criando uma chave secreta pro db
# Para estudo, está sendo definida com uma string
app.config['SECRET_KEY'] = "your_secret_key"

# Definindo o caminho para o SQLAlchemy se conetar ao db
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ADMIN123@127.0.0.1:3306/flask-auth-crud"

login_manager = LoginManager()

# Inicializando o app de db e login_manager (de database.py) com o 'app.py'
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# --------------------------------------------------------------------------------------------
# Rota Login

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

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
  login_user(user_db)
  return jsonify({"message": "Autenticação realizada com sucesso"})

# --------------------------------------------------------------------------------------------
# Rota Logout

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})

# --------------------------------------------------------------------------------------------
# Rota Create User (Cadastro de novos usuarios)

@app.route("/user", methods=["POST"])
def create_user():
  data = request.get_json()
  username = data["username"]
  password = data["password"]

  # se alguma das infos for vazia, volta erro
  if not username or not password:
    return jsonify({"message": "Dados inválidos"}), 400
  
  # do contrario, cadastra
  user = User(username=username, password=password)
  db.session.add(user)
  
  db.session.commit()

  return jsonify({"message": "Usuario cadastrado com sucesso"})

# --------------------------------------------------------------------------------------------
# Rota Read User

@app.route("/user/<int:user_id>", methods=["GET"])
@login_required
def read_user(user_id):
  user = User.query.get(user_id)

  # se o user com aquele id não for encontrado, volta erro
  if not user:
    return jsonify({"message": "Usuario não encontrado"}), 404
  
  # do contrario, retorna as infos do user
  return jsonify({"username": user.username})

# --------------------------------------------------------------------------------------------
# Rota Update User

@app.route("/user/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
  data = request.get_json()
  user = User.query.get(user_id)

  # se o user com aquele id não for encontrado, volta erro
  if not user:
    return jsonify({"message": "Usuario não encontrado"}), 404

  # se nao existir campo password na request, volta erro
  if not data.get("password"):
    return jsonify({"message": "O campo 'password' é obrigatório para atualizar user"}), 400
  
  # do contrario, atualiza o user
  user.password = data["password"]
  db.session.commit()

  return jsonify({"message": f"Usuario {user_id} atualizado com sucesso"})

# --------------------------------------------------------------------------------------------
# Rota Delete User

@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
  # se o user_id for igual ao do usuario que está logado, volta erro
  if user_id == current_user.id:
    return jsonify({"message": "Não é possível deletar o usuário logado"}), 400

  user = User.query.get(user_id)

  # se o user com aquele id não for encontrado, volta erro
  if not user:
    return jsonify({"message": "Usuario não encontrado"}), 404
  
  # do contrario, deleta o user
  db.session.delete(user)
  db.session.commit()
  return jsonify({"message": f"Usuario {user_id} deletado com sucesso"})

# --------------------------------------------------------------------------------------------
# Rota Hello World (para testes iniciais)

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "hello world!"

# --------------------------------------------------------------------------
# Rota para inicialização manual

if __name__ == "__main__":
  app.run(debug=True)

# --------------------------------------------------------------------------