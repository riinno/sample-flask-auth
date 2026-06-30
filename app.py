# by Riinno, 2026

# -------------------------------------------------------------
#Importação de dependencias e variaveis base

from flask import Flask
from models.user import User
from database import db

app = Flask(__name__)

# Criando uma chave secreta pro db
# Para estudo, está sendo definida com uma string
app.config['SECRET_KEY'] = "your_secret_key"

# Definindo o caminho para o SQLAlchemy se conetar ao db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

# Inicializando o app de db (de database.py) com o 'app.py'
db.init_app(app)

# -------------------------------------------------------------
# Rota Hello World (para testes iniciais)

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "hello world!"

# -------------------------------------------------------------
# Rota para inicialização manual

if __name__ == "__main__":
  app.run(debug=True)

# -------------------------------------------------------------