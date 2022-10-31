import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User
from App.controllers import *

from App.main import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob")
        user.set_password("bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob")
        user.set_password(password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob")
        user.set_password(password)
        assert user.check_password(password)

    def test_new_student(self):
        student = create_student(id=1, fName = "john", lName =  "doe")
        assert student == "pass"
    
    def test_new_review(self):
        review = create_review("Testing", 1, 1)
        assert review == "pass"

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    def test_create_student(self):
        newStudent = create_student(1, "john", "doe")
        newstudentCheck = get_student(1)
        assert newstudentCheck.firstName == "john"

    def test_update_student(self):
        newStudent = create_student(2, "jane", "smiths")
        update_student(2, "jane", "smith")
        newstudentCheck = get_student(2)
        assert newstudentCheck.lastName == "smith"

    def test_get_all_students(self):
        students = get_all_students()
        assert students[0].firstName == "john"

    def test_create_review(self):
        create_review("Testing", 1, 1)
        newReview = get_review_by_id(1)
        assert newReview.review == "Testing"

    def test_get_all_reviews(self):
        reviews = get_all_reviews()
        assert reviews[0].review == "Testing"

    def test_get_student_by_id(self):
        student = get_student(1)
        assert student.firstName == 'john'

    def test_upvote(self):
        upvote_review(1)
        reviewCheck = get_review_by_id(1)
        assert reviewCheck.karma == 1

    def test_downvote(self):
        downvote_review(2)
        reviewCheck = get_review_by_id(2)
        assert reviewCheck.karma == -1
    

    
