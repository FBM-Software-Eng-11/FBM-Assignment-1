from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    review = db.relationship('Review', backref='user', lazy=True,cascade="all, delete-orphan" )

    def __init__(self, username):
        self.username = username

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)