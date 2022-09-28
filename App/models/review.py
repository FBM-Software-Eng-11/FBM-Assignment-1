from App.database import db

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  karma =  db.Column(db.Integer,unique=False,nullable=False)
  review = db.Column(db.String(200))
  studentId = db.Column(db.Integer, db.ForeignKey('student.id'))
  userId = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, review, studentId, userId):
    self.review = review
    self.studentId = studentId
    self.userId = userId
    self.karma = 0

  def toDict(self):
      return{
          'id': self.id,
          'student_ID': self.studentId,
          'user_ID': self.userId,
          'review': self.review,
          'karma': self.karma,
      }