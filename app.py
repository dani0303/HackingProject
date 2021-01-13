from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy






app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'sEcReTkEy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dan/Desktop/HackingProject/sqlite3/database.db'

db = SQLAlchemy(app)




class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    grade = db.Column(db.String(4))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))




class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    accessCode = db.Column(db.String(4))
    students = db.relationship('Student', backref = 'teacher')


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




class SearchForm(FlaskForm):
    Code = StringField('accessCode', validators=[InputRequired(), Length(max=4)])


@app.route('/', methods=['POST', 'GET'])##begins with page with two buttons "student" or "teacher"
def index2():
    return render_template('test.html')




@app.route('/teacherCode', methods=['POST', 'GET'])
def Codeform():
    form = SearchForm()

    if form.validate_on_submit():
        teacherCode = Teacher.query.filter_by(Code = form.Code.data).first()
        if teacherCode:
            if teacherCode.accessCode == form.Code.data:
                return redirect(url_for('index2'))
        return '<h1>The person you are looking for is not here</h1>'

    return render_template('index.html', form=form)




@app.route('/studentLogin', methods=['GET', 'POST'])
def Studentlogin():
    form = StudentLoginForm()

    if form.validate_on_submit():
        studentLogin = Student.query.filter_by(username=form.username.data).first()
        if studentLogin:
            if studentLogin.password == form.password.data:
                return  redirect(url_for('Codeform'))

    return render_template("studentLogin.html", form=form)




@app.route('/teacherLogin', methods=['GET', 'POST'])
def Teacherlogin():
    form = TeacherLoginForm()

    if form.validate_on_submit():
        user = Teacher.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('index2'))
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('teacherLogin.html', form=form)




@app.route('/StudentSignUp', methods=['GET', 'POST'])
def StudentSignUp():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_student)
        db.session.commit()
        students = Student.query.all()
        return redirect(url_for('Studentlogin'))

    return render_template("StudentSignUp.html", form=form)




@app.route('/TeacherSignUp', methods=['GET', 'POST'])
def TeacherSignUp():
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        new_teacher = Teacher(username=form.username.data, email=form.email.data, password=form.password.data, accessCode=form.accessCode.data)
        db.session.add(new_teacher)
        db.session.commit()
        return '<h1>Teacher added</h1>'

    return render_template("TeacherSignUp.html", form=form)



  
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)