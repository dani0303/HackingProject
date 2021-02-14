from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'sEcReTkEy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dan/Desktop/HackingProject/sqlite3/database.db'
db = SQLAlchemy(app)
from HackingProject import routes