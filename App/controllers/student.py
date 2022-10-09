from App.models import Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_all_students():
    return Student.query.all()

def get_student(id):
  student = Student.query.filter_by(id=id).first()
  return student

def get_student_by_name(firstName, lastName):
  student = Student.query.filter_by(firstName=firstName,lastName=lastName).first()
  return student

def create_student(id, fName, lName):
    student = Student(id = id, firstName=fName, lastName=lName)
    try:
        db.session.add(student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'fail'
    return 'pass'

def update_student(id,fName, lName):
  student = get_student(id)
  student.firstName = fName,
  student.lastName = lName,
  db.session.add(student)
  db.session.commit()
  return 'Updated', 201