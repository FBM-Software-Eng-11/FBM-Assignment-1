from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), unique=True, nullable=False) 
    lastName = db.Column(db.String(120), nullable=False)
    review = db.relationship('Review', backref='student',lazy=True,cascade="all, delete-orphan")

    def __init__(self,firstName,lastName):
        self.firstName = firstName
        self.lastName = lastName

    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.firstName,
            'last_name': self.lastName,
        }