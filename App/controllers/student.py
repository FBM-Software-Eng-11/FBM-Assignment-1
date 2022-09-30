from App.models import Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_all_students():
    return Student.query.all()

def get_student(id):
  student = Student.query.filter_by(id=id).first()
  return student

def create_student(firstName, lastName):
    student = Student(firstName=firstName, lastName=lastName)
    try:
        db.session.add(student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'fail'
    return 'pass'

def update_student(id,firstName, lastName):
  student = get_student(id)
  student.firstName = firstName,
  student.lastName = lastName,
  db.session.add(student)
  db.session.commit()