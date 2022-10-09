from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, json, jsonify
from flask import Flask, request, url_for, g
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required, login_manager
from .forms import SignUp, LogIn, AddReview, AddStudent
from ..controllers.review import *
from App.controllers import *


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)

@index_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  review_form = AddReview()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return render_template('reviews.html', form=review_form) # redirect to main page if login successful
  flash('Invalid credentials')
  return render_template('login.html',form =form)


@index_views.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template

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

@index_views.route('/', methods=['GET'])
def index_page():
    form = LogIn()
    return render_template('login.html', form=form)

@index_views.route('/reviews', methods=['POST'])
@login_required
def create_review():
    data = request.get_json()
    create_review(review=data['review'],studentId = data['studentId'], userId =current_identity.id)
    return render_template('reviews.html', form=form)

@index_views.route('/reviews', methods=['GET'])
@login_required
def get_review():
    reviews = get_all_reviews()
    if reviews is None:
        reviews = []
    form = AddReview()
    return render_template('reviews.html', reviews=reviews, form=form)

@index_views.route('/reviews/<id>', methods=['GET'])
@login_required
def get_review_id():
    reviews = get_review(id, current_identity.id)
    return render_template('review.html', reviews=reviews)

@index_views.route('/reviews/<id>', methods=['PUT'])
@login_required
def update_review(id):
  review = get_review(id, current_identity.id)
  if review == None:
    return 'Invalid id or unauthorized'
  data = request.get_json()
  if 'review' in data: # we can't assume what the user is updating wo we check for the field
    review.review = data['review']
  if 'karma' in data:
    review.karma = data['karma']
  db.session.add(review)
  db.session.commit()
  return 'Updated', 201

@index_views.route('/reviews/<id>', methods=['PUT'])
@login_required
def delete_review_by_id(id):
  delete_review(id, current_identity.id)
  return 'Deleted', 204
  
@index_views.route('/createStudent',methods=['GET'])
@login_required
def create_new_student():
    students = get_all_students()
    if students is None:
        students = []
    form = AddStudent()
    return render_template('addstudent.html', form=form, students = students)

@index_views.route('/createStudent',methods=['POST'])
@login_required
def create_new_student_action():
    data = request.form
    student = create_student(fName = data['firstName'], lName = data['lastName'])
    return student
    
    return render_template('addstudent.html' , form=form, students = students)