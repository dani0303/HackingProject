from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



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
    grade = StringField('grade', validators=[InputRequired(), Length(max=4)])
    teacherID = StringField('teacherID', validators=[InputRequired(), Length(max=2)])




class TeacherRegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    accessCode = StringField('accessCode', validators=[InputRequired(), Length(max=4)])



@app.route('/', methods=['POST', 'GET'])##begins with page with two buttons "student" or "teacher"
def index2():
    return render_template('test.html')



@app.route('/search', methods=['POST', 'GET'])
def Codeform():
    form = SearchForm()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form['tag']
        search = "%{}%".format(tag)
        teachers = Teacher.query.filter(Teacher.accessCode.like(search)).all()
        return render_template('Search.html', teachers=teachers, tag=tag)
            
    return render_template('Search.html', form=form)


@app.route('/teacherLogin', methods=['GET', 'POST'])
def Teacherlogin():
    form = TeacherLoginForm()

    if form.validate_on_submit():
        user = Teacher.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('viewStudents', usr=user.id))
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('teacherLogin.html', form=form)



@app.route('/<usr>', methods=['GET', 'POST'])
def viewStudents(usr):
    classes = Student.query.filter(Student.teacher_id.like(usr)).all()
    ##return f"<h1>{usr}</h1>"
    return render_template('viewStudents.html', classes=classes)


@app.route('/TeacherSignUp', methods=['GET', 'POST'])
def TeacherSignUp():
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        hashed_teacher = generate_password_hash(form.password.data, method='sha256')
        new_teacher = Teacher(username=form.username.data, email=form.email.data, password=hashed_teacher, accessCode=form.accessCode.data)
        db.session.add(new_teacher)
        db.session.commit()
        return render_template("teacherLogin.html")

    return render_template("TeacherSignUp.html", form=form)


@app.route('/studentLogin', methods=['GET', 'POST'])
def Studentlogin():
    form = StudentLoginForm()##create form where user will input their information(username and passwd)
    if form.validate_on_submit():##when user clicks submit
        studentLogin = Student.query.filter_by(username=form.username.data).first()
        ##studentLogin will create an object where it search for the username given in the form
        if studentLogin:##if the object is created
            if studentLogin.password == form.password.data:
                ##studentLogin.password will search for the password for the username the user typed in the search box
                return  "<h1>Login Successful</h1>"##will display this on the screen when login was successful

    return render_template("studentLogin.html", form=form)



@app.route('/StudentSignUp', methods=['GET', 'POST'])
def StudentSignUp():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        hashed_student = generate_password_hash(form.password.data, method='md5')
        new_student = Student(username=form.username.data, email=form.email.data, password=hashed_student, grade=form.grade.data, teacher_id=form.teacherID.data)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('Studentlogin'))

    return render_template("StudentSignUp.html", form=form)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)