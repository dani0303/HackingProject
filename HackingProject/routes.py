from flask import render_template, redirect, url_for, request
from HackingProject import app
from HackingProject.models import Student, Teacher
from HackingProject.forms import StudentLoginForm, TeacherLoginForm, StudentRegisterForm, TeacherRegisterForm, SearchForm

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
                return redirect(url_for('viewStudents', usr=user.username))
        
        return '<h1>Wrong Username or Password</h1>'

    return render_template('teacherLogin.html', form=form)



@app.route('/<usr>', methods=['GET', 'POST'])
def viewStudents(usr):
    teachers = Teacher.query.filter(Teacher.username.like(usr)).first()
    ##return f"<h1>{usr}</h1>"
    return render_template('viewStudents.html', teachers=teachers)


@app.route('/TeacherSignUp', methods=['GET', 'POST'])
def TeacherSignUp():
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        new_teacher = Teacher(username=form.username.data, email=form.email.data, password=form.password.data, accessCode=form.accessCode.data)
        db.session.add(new_teacher)
        db.session.commit()
        return render_template("teacherLogin.html")

    return render_template("TeacherSignUp.html", form=form)


@app.route('/studentLogin', methods=['GET', 'POST'])
def Studentlogin():
    form = StudentLoginForm()
    if form.validate_on_submit():
        studentLogin = Student.query.filter_by(username=form.username.data).first()
        if studentLogin:
            if studentLogin.password == form.password.data:
                return  redirect(url_for('Codeform'))

    return render_template("studentLogin.html", form=form)



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


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")