from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SECRET_KEY'] = 'sEcReTkEy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dan/Desktop/HackingProject/sqlite3/database.db'
Bootstrap(app)
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref = 'owner')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))  



class StudentUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    ##email = db.Column(db.String(50), unique=True)
    ##password = db.Column(db.String(80))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))




class TeacherUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    ##email = db.Column(db.String(50), unique=True)
    ##password = db.Column(db.String(80))
    ##accessCode = db.Column(db.String(5))
    students = db.relationship('StudentUser', backref = 'teacher')


class StudentLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('remember me')




class TeacherLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    accessCode = StringField('accessCode', validators=[InputRequired(), Length(max=4)])
    remember = BooleanField('remember me')



class StudentRegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])




class TeacherRegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    accessCode = StringField('accessCode', validators=[InputRequired(), Length(max=4)])




@app.route('/', methods=['POST', 'GET'])##begins with page with two buttons "student" or "teacher"
def index2():
    return render_template('test.html')




@app.route('/studentLogin', methods=['GET', 'POST'])
def Studentlogin():
    form = StudentLoginForm()

    if form.validate_on_submit():
        user = StudentUser.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return render_template("dashboard.html")
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('studentLogin.html', form=form)




@app.route('/teacherLogin', methods=['GET', 'POST'])
def Teacherlogin():
    form = TeacherLoginForm()

    if form.validate_on_submit():
        user = StudentUser.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return render_template("dashboard.html")
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('teacherLogin.html', form=form)




@app.route('/StudentSignUp', methods=['GET', 'POST'])
def StudentSignUp():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        new_student = StudentUser(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("team_members"))

    return render_template("StudentSignUp.html", form=form)




@app.route('/TeacherSignUp', methods=['GET', 'POST'])
def TeacherSignUp():
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        new_teacher = TeacherUser(username=form.username.data, email=form.email.data, password=form.password.data, accessCode=form.accessCode.data)
        db.session.add(new_teacher)
        db.session.commit()
        return '<h1>Teacher added</h1>'

    return render_template("TeacherSignUp.html", form=form)



  
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)