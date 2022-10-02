from flask import Blueprint, render_template, jsonify, request, send_from_directory,flash, redirect, url_for
from flask_jwt import jwt_required
from flask_login import LoginManager, current_user, login_user, login_required, login_manager, login_required


from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    create_student
)

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/students')
def get_students_page():
    students = get_all_students_json()
    return jsonify(students)

@user_views.route('/api/reviews')
def get_reviews_page():
    reviews = get_all_reviews_json()
    return jsonify(reviews)



@user_views.route('/signup', methods=['POST'])
def signup_user():
    data = request.form
    stat = create_user(data['username'], data['password'])
    if(stat == 'pass'):
        flash('Account Created!')
        return render_template('loginTesting.html')
    else:
        flash('Username or Email already in use!')
        return render_template('signupTesting.html')

@user_views.route('/auth',methods=['POST'])
def logsIn_user():
    data = request.form
    user = authenticate(data['username'], data['password'])
    if user == None:
        flash('Wrong Username or Password!')
        return render_template('loginTesting.html')
    login_user(user)
    return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')

@user_views.route('/home')
@login_required
def home():
    students = get_all_students()
    reviews = get_all_test()
    return render_template('reviewsTesting.html', students = students, reviews = reviews)

@user_views.route('/createStudent',methods=['POST'])
@login_required
def create_new_student():
    data = request.form
    newStudent = create_student(fname=data['first_name'], lname=data['last_name'])
    if(newStudent == 'pass'):
        flash('Student Added')
        return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')
    else:
        flash('Error Adding Student')
        return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')

@user_views.route('/createReview',methods=['POST'])
@login_required
def create_new_review():
    data = request.form
    newReview = create_review(review = data['review'], studentId= data['id'], userId= current_user.id)
    if(newReview == 'pass'):
        flash('Review Added')
        return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')
    else:
        flash('Error Adding Review')
        return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')

@user_views.route('/upvote/<id>')
@login_required
def upvote(id):
    result = upvote_review(id)
    return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')

@user_views.route('/downvote/<id>')
@login_required
def downvote(id):
    result = downvote_review(id)
    return redirect('https://8080-fbmsoftware-fbmassignme-nq00kjdef7x.ws-us69.gitpod.io/home')

