from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, json, jsonify
from flask import Flask, request, url_for, g
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, login_manager
from ..controllers.review import *
from App.controllers import *


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/')
def home():
  return render_template('index.html')

#Logins in the user and redirects
@index_views.route('/login', methods=['POST'])
def loginAction():
  userdata = request.get_json()
  user = User.query.filter_by(username = userdata['username']).first()
  if user and user.check_password(userdata['password']): # check credentials
    flash('Logged in successfully.') # send message to next page
    login_user(user,True) # login the user
    return 'User logged in'
  return 'Invalid credentials'

#Allows user to sign in and redirects as needed
@index_views.route('/signup', methods=['POST'])
def signup_action():
  userdata = request.get_json()
  newuser = User(username=userdata['username']) # create user object
  newuser.set_password(userdata['password']) # set password
  try:
    db.session.add(newuser)
    db.session.commit() 
  except IntegrityError: 
    db.session.rollback()
    return 'username already exists'
  return 'user created'

#Renders the main page with the reviews
@index_views.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    reviews = get_all_reviews()
    reviews = [review.toDict() for review in reviews]
    return jsonify(reviews)

#Creates a review and should rerender the page
@index_views.route('/reviews', methods=['POST'])
@login_required
def create_review_action():
    data = request.get_json()
    student = get_student(data['studentId'])
    if student is None:
      return "Student not found"
    result = create_review(review=data['review'],studentId = data['studentId'], userId =current_user.id)
    if result == "pass":
      return 'Review created'
    return 'Failed to create review'

#Get a review by an id
@index_views.route('/reviews/<UserId>', methods=['GET'])
@login_required
def get_review_id(UserId):
    reviews = get_review(userId=UserId)
    reviews = [review.toDict() for review in reviews]
    return jsonify(reviews)

#Create student and should rerender the page
@index_views.route('/createStudent',methods=['POST'])
@login_required
def create_new_student_action():
    data = request.get_json()
    student = create_student(id = data['id'], fName = data['firstName'], lName = data['lastName'])
    students = get_all_students()
    if student == "pass":
      return 'Student Created'
    return 'Student not created'

#Search for student by ID
@index_views.route('/student/<studentId>',methods=['GET'])
@login_required
def search_student(studentId):
  student = get_student(studentId)
  return student.toDict()

#update student
@index_views.route('/student/<id>',methods=['PUT'])
@login_required
def update_student_by_id(id):
  student = get_student(id)
  if student == None:
    return 'Student does not exist'
  data = request.get_json()
  update_student(id = data['id'], fName = data['firstName'], lName = data['lastName'])
  return 'Student updated'

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


