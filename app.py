from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
Bootstrap(app)

class LoginForms 
##Push this code please
@app.route('/')
def index2():
    return render_template("index2.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)