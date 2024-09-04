from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(150), nullable=False)
  lastname = db.Column(db.String(150), nullable=False)
  username = db.Column(db.String(150), nullable=False, unique=True)
  email = db.Column(db.String(150), nullable=False, unique=True)
  contact = db.Column(db.String(15), nullable=False)
  password = db.Column(db.String(150), nullable=False)