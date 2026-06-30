# by Riinno, 2026

# -------------------------------------------
#Importação de dependencias e variaveis base

from flask import Flask

app = Flask(__name__)

# -------------------------------------------
# Rota Hello World (para testes iniciais)

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "hello world!"

# -------------------------------------------
# Rota para inicialização manual

if __name__ == "__main__":
  app.run(debug=True)

# -------------------------------------------