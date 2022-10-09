from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, json, jsonify
from flask import Flask, request, url_for, g
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, login_manager
from .forms import SignUp, LogIn, AddReview, AddStudent
from ..controllers.review import *
from App.controllers import *


index_views = Blueprint('index_views', __name__, template_folder='../templates')

#Renders the login page
@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)

#Logins in the user and redirects
@index_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  review_form = AddReview()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user,True) # login the user
        return render_template('reviews.html', form=review_form) # redirect to main page if login successful
  flash('Invalid credentials')
  return render_template('login.html',form =form)

#reders the signup page
@index_views.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template

#Allows user to sign in and redirects as needed
@index_views.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    return render_template('index.html')
  flash('Error invalid input!')
  return render_template('signup.html', form = form)

#Renders the main page with the reviews
@index_views.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    reviews = get_all_reviews()
    if reviews is None:
        reviews = []
    form = AddReview()
    students = get_all_students()
    return render_template('reviews.html', reviews=reviews, form=form, students= students)

#Creates a review and should rerender the page
@index_views.route('/reviews', methods=['POST'])
@login_required
def create_review_action():
    data = request.form
    result = create_review(review=data['review'],studentId = data['studentId'], userId =current_user.id)
    reviews = get_all_reviews()
    if reviews is None:
        reviews = []
    form = AddReview()
    students = get_all_students()
    return render_template('reviews.html', reviews=reviews, form=form, students = students)

#Get a review by an id
@index_views.route('/reviews/<id>', methods=['GET'])
@login_required
def get_review_id(id):
    reviews = get_review(id = id , userId=current_user.id)
    return reviews.toDict()
    form = AddReview()
    return render_template('reviews.html', reviews=reviews, form=form)
  
  #Render the create student page
@index_views.route('/createStudent',methods=['GET'])
@login_required
def create_new_student():
    students = get_all_students()
    if students is None:
        students = []
    form = AddStudent()
    return render_template('addstudent.html', form=form, students = students)

#Create student and should rerender the page
@index_views.route('/createStudent',methods=['POST'])
@login_required
def create_new_student_action():
    data = request.form
    student = create_student(id = data['id'], fName = data['firstName'], lName = data['lastName'])
    students = get_all_students()
    if students is None:
        students = []
    form = AddStudent()
    return render_template('addstudent.html' , form=form, students = students)

#Search for student by ID
@index_views.route('/student/<id>',methods=['GET'])
@login_required
def search_student(id):
  student = get_student(id)
  return student.toDict()

#update student
@index_views.route('/student/<id>',methods=['PUT'])
@login_required
def update_student_by_id(id):
  student = get_student(id)
  if student == None:
    return 'Student does not exitst'
  data = request.form
  update_student(id = data['id'], fName = data['firstName'], lName = data['lastName'])

@index_views.route('/upvote/<id>')
@login_required
def upvote(id):
    result = upvote_review(id)
    return 'pass'

@index_views.route('/downvote/<id>')
@login_required
def downvote(id):
    result = downvote_review(id)
    return 'pass'


