from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

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



class JoinForm(FlaskForm):
    join = BooleanField('Join')



class SearchForm(FlaskForm):
    Code = StringField('Pin', validators=[InputRequired(), Length(max=4)])
class JoinForm(FlaskForm):
    Join = BooleanField('Join')