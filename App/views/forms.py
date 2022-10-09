from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Email, NumberRange

class SignUp(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AddReview(FlaskForm):
    studentId = StringField('studentId', validators =[InputRequired()])
    review = StringField('review', validators =[InputRequired()])
    karma = IntegerField('karma', validators =[InputRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Add', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AddStudent(FlaskForm):
    id = IntegerField('StudentID', validators =[InputRequired()])
    firstName = StringField('firstName', validators =[InputRequired()])
    lastName = StringField('lastName', validators =[InputRequired()])