from HackingProject import db

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