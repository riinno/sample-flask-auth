# Code by Riinno, 2026

# -------------------------------------------------------------------------------
#Importação de dependencias

from database import db
from flask_login import UserMixin

# -------------------------------------------------------------------------------
# Definição da classe

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) # ID, identifica um usuário no DB
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)

# -------------------------------------------------------------------------------