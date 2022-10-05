from flask import Blueprint, redirect, render_template, request, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import LoginManager, current_user, login_user, login_required
from .forms import SignUp, LogIn, AddReview
from ..controllers.review import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    form = LogIn()
    return render_template('login.html', form=form)

@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)

@index_views.route('/signup', methods=['GET'])
def signup_page():
    form = SignUp()
    return render_template('signup.html', form=form)

@index_views.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    review = Review(karam=data['karam'], review=data['review'], studentId=data['studentId'], userId=current_identity.id)
    create_review(review, data['studentId'], current_identity.id)
    return render_template('reviews.html', form=form)

@index_views.route('/reviews', methods=['GET'])
@jwt_required()
def get_review():
    reviews = get_all_reviews()
    if reviews is None:
        reviews = []
    form = AddReview()
    return render_template('reviews.html', reviews=reviews, form=form)

@index_views.route('/reviews/<id>', methods=['GET'])
@jwt_required()
def get_review_id():
    reviews = get_review(id, current_identity.id)
    return render_template('review.html', reviews=reviews)

@index_views.route('/reviews/<id>', methods=['PUT'])
@jwt_required()
def update_review(id):
  review = get_review(id, current_identity.id)
  if review == None:
    return 'Invalid id or unauthorized'
  data = request.get_json()
  if 'review' in data: # we can't assume what the user is updating wo we check for the field
    review.review = data['review']
  if 'karma' in data:
    review.karam = data['karma']
  db.session.add(review)
  db.session.commit()
  return 'Updated', 201

@index_views.route('/reviews/<id>', methods=['PUT'])
@jwt_required()
def delete_todo(id):
  delete_review(id, current_identity.id)
  return 'Deleted', 204
  
