from App.models import Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_all_students():
    return Student.query.all()

def get_student(id):
  student = Student.query.filter_by(id=id).first()
  return student

def create_student(fname, lname):
    student = Student(firstName = fname, lastName = lname)
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

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    student = [student.toJSON() for student in students]
    return student