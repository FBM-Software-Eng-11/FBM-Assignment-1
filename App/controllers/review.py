from App.models import Student, User, Review
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_all_reviews():
    return Review.query.all()

def get_review(id, userId):
  review = Review.query.filter_by(id=id, userId=userId).first()
  return review

def create_review(review, studentId, userId):
    review = Review(review = review, studentId = studentId, userId = userId)
    try:
        db.session.add(review)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'fail'
    return 'pass'

def upvote_review(id):
  review = Review.query.filter_by(id=id).first()
  review.karma += 1
  db.session.add(review)
  db.session.commit()

def downvote_review(id):
  review = Review.query.filter_by(id=id).first()
  review.karma -= 1
  db.session.add(review)
  db.session.commit()

def update_review(id, review, userId):
  new_review = get_review(id, userId)
  new_review.review = review,
  db.session.add(new_review)
  db.session.commit()

def delete_review(id, userId):
  review = get_review(id, userId)
  db.session.delete(review)
  db.session.commit()