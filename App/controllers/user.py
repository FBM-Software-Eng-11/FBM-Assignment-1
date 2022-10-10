from App.models import User
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_all_users():
    return User.query.all()

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users