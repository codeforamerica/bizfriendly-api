import unittest, requests, json

from bizfriendly import app
from bizfriendly.models import *
from bizfriendly.routes import *


class bf_tests(unittest.TestCase):
    
    def setUp(self):
        # Set up the database settings
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost/bizfriendly_test'
        app.config['SECRET_KEY'] = '123456'
        app.config['TESTING'] = True
        db.create_all()
        self.app = app.test_client()
        
        # Fill up the DB
        self.test_user = {
            "name" : "Test User",
            "email" : "TestUser@TestEmail.com".lower(),
            "password" : "Test Password"
        }
        test_user_obj = Bf_user(**self.test_user)
        db.session.add(test_user_obj)
        
        self.test_category = {
            "name" : "Test Category",
            "description" : "Test description",
            "state" : "published",
            "creator_id" : 1
        }
        test_category_obj = Category(**self.test_category)
        db.session.add(test_category_obj)

        self.test_service = {
            "name" : "Test Service",
            "url" : "Test Url",
            "short_description" : "Test short description",
            "long_description" : "Test long description",
            "additional_resources" : "Test additional resources",
            "tips" : "Test tips",
            "state" : "published",
            "category_id" : 1,
            "creator_id" : 1
        }
        test_service_obj = Service(**self.test_service)
        db.session.add(test_service_obj)

        self.test_lesson = {
            "name" : "Test Lesson",
            "description" : "Test short description",
            "ease" : "Test ease",
            "state" : "published",
            "service_id" : 1,
            "creator_id" : 1
        }
        test_lesson_obj = Lesson(**self.test_lesson)
        db.session.add(test_lesson_obj)

        self.test_step = {
            "step_type" : "Test step type",
            "step_number" : 1,
            "step_text" : "Test step text",
            "trigger_endpoint" : "Test trigger endpoint",
            "place_in_collection" : 'first',
            "trigger_check" : "Test trigger check",
            "trigger_value" : "Test trigger value",
            "thing_to_remember" : "Test thing to remember",
            "lesson_id" : 1,
            "creator_id" : 1
        }
        test_step_obj = Step(**self.test_step)
        db.session.add(test_step_obj)

        db.session.commit()

        self.headers = [('Content-Type', 'application/json')]

    def tearDown(self):
        db.drop_all()


    # Test API -----------------------

    def test_headers(self):
        response = self.app.get('/api/v1/categories')
        assert response.headers['Access-Control-Allow-Origin']  == '*'
        assert response.headers['Content-Type']  == 'application/json'

    def test_categories(self):
        response = self.app.get('/api/v1/categories')
        response = json.loads(response.data)
        assert isinstance(response, dict)
        assert isinstance(response['objects'], list)
        assert isinstance(response['objects'][0]['id'], int)
        assert isinstance(response['objects'][0]['name'], unicode)
        assert isinstance(response['objects'][0]['description'], unicode)
        assert isinstance(response['objects'][0]['state'], unicode)
        assert isinstance(response['objects'][0]['services'], list)
        assert isinstance(response['objects'][0]['creator_id'], int)

    def test_categories_post(self):
        self.test_category['name'] = 'New Test Category'
        data = json.dumps(self.test_category)
        response = self.app.post('api/v1/categories', data=data, headers=self.headers)
        assert response.status_code == 201

    def test_services(self):
        response = self.app.get('/api/v1/services')
        response = json.loads(response.data)
        assert isinstance(response, dict)
        assert isinstance(response['objects'], list)
        assert isinstance(response['objects'][0]['id'], int)
        assert isinstance(response['objects'][0]['name'], unicode)
        assert isinstance(response['objects'][0]['url'], unicode)
        assert isinstance(response['objects'][0]['short_description'], unicode)
        assert isinstance(response['objects'][0]['long_description'], unicode)
        assert isinstance(response['objects'][0]['additional_resources'], unicode)
        assert isinstance(response['objects'][0]['tips'], unicode)
        assert isinstance(response['objects'][0]['state'], unicode)
        assert isinstance(response['objects'][0]['category_id'], int)
        assert isinstance(response['objects'][0]['lessons'], list)
        assert isinstance(response['objects'][0]['creator_id'], int)

    def test_services_post(self):
        self.test_service['name'] = 'New Test Service'
        data = json.dumps(self.test_service)
        response = self.app.post('api/v1/services', data=data, headers=self.headers)
        assert response.status_code == 201

    def test_lessons(self):
        response = self.app.get('/api/v1/lessons')
        response = json.loads(response.data)
        assert isinstance(response, dict)
        assert isinstance(response['objects'], list)
        assert isinstance(response['objects'][0]['id'], int)
        assert isinstance(response['objects'][0]['name'], unicode)
        assert isinstance(response['objects'][0]['ease'], unicode)
        assert isinstance(response['objects'][0]['description'], unicode)
        assert isinstance(response['objects'][0]['state'], unicode)
        assert isinstance(response['objects'][0]['service_id'], int)
        assert isinstance(response['objects'][0]['steps'], list)
        assert isinstance(response['objects'][0]['creator_id'], int)

    def test_lessons_post(self):
        self.test_lesson['name'] = 'New Test lesson'
        data = json.dumps(self.test_lesson)
        response = self.app.post('api/v1/lessons', data=data, headers=self.headers)
        assert response.status_code == 201

    def test_steps(self):
        response = self.app.get('/api/v1/steps')
        response = json.loads(response.data)
        assert isinstance(response, dict)
        assert isinstance(response['objects'], list)
        assert isinstance(response['objects'][0]['id'], int)
        assert isinstance(response['objects'][0]['step_type'], unicode)
        assert isinstance(response['objects'][0]['step_number'], int)
        assert isinstance(response['objects'][0]['step_text'], unicode)
        assert isinstance(response['objects'][0]['trigger_endpoint'], unicode)
        assert isinstance(response['objects'][0]['place_in_collection'], unicode)
        assert isinstance(response['objects'][0]['trigger_check'], unicode)
        assert isinstance(response['objects'][0]['trigger_value'], unicode)
        assert isinstance(response['objects'][0]['thing_to_remember'], unicode)
        assert isinstance(response['objects'][0]['lesson_id'], int)
        assert isinstance(response['objects'][0]['creator_id'], int)

    def test_steps_post(self):
        data = json.dumps(self.test_step)
        response = self.app.post('api/v1/steps', data=data, headers=self.headers)
        assert response.status_code == 201

    # # Test Admin --------------------------------

    def test_admin(self):
        response = self.app.get('/api/admin/')
        assert response.headers['content-type'] == 'text/html; charset=utf-8'

    def test_admin_bad_login(self):
        response = self.app.get('/login')
        assert response.headers['content-type'] == 'text/html; charset=utf-8'

    # Test Sign Up and Sign In -------------------

    def test_signup_new_email(self):
        self.test_user['email'] = "NewTestUser@TestEmail.com"
        response = self.app.post('/signup', data=self.test_user)
        assert response.status_code == 200 
        response = json.loads(response.data)
        assert "id" in response
        assert "name" in response
        assert response["name"] == "Test User"
        assert "email" in response
        assert "access_token" in response

    def test_signup_same_email(self):
        response = self.app.post('/signup', data=self.test_user)
        assert response.status_code == 401
        response = json.loads(response.data)
        assert "error" in response
        assert response["error"] == 'Someone has already signed up with that email.'

    def test_signin(self):
        response = self.app.post('/signin', data=self.test_user)
        assert response.status_code == 200 
        response = json.loads(response.data)
        assert "id" in response
        assert "name" in response
        assert response["name"] == "Test User"
        assert "email" in response
        assert "access_token" in response

    def test_signin_bad(self):
        self.test_user['password'] = "1234"
        response = self.app.post('/signin', data=self.test_user)
        assert response.status_code == 401
        response = json.loads(response.data)
        assert "error" in response
        assert response["error"] == "Couldn't find your email and password."

    # Test Routes ---------------------------------
    
    def test_get_data_on_attribute_path(self):
        attributes = ['name',"7",0]
        json_data = {
            "fake" : False,
            "name" : {
                "fake" : False,
                7 : {
                    "fake" : False,
                    0 : True
                }
            }
        }
        assert get_data_on_attribute_path(json_data, attributes)

    def test_boolify(self):
        assert boolify("True")
        assert boolify("true")
        assert not boolify("False")
        assert not boolify("false")

    def test_autoconvert(self):
        assert type(autoconvert("100") == int)
        assert type(autoconvert("false") == bool)
        assert type(autoconvert("12.07") == float)
        
    def test_check_for_new_no_original_count(self):
        response = self.app.post('/signin', data=self.test_user)
        response = json.loads(response.data)
        auth = response["access_token"]
        self.headers = [("Content-Type", "application/x-www-form-urlencoded"),("Authorization", auth)]

        self.test_connection = {
            "service" : "trello",
            "service_access" : "3ad4b59c2f9879726aed00f9ecc3d5a6219d854e4925f44ff5ed53994d424e93"
        }
        self.app.post('/create_connection', data=self.test_connection, headers=self.headers)
        
        data = {
            "currentStep[id]" : 0,
            "currentStep[name]" : "test Step",
            "currentStep[stepType]" : "check_for_new",
            "currentStep[stepNumber]" : 1,
            "currentStep[stepText]" : "Test Step Text",
            "currentStep[triggerEndpoint]" : "https://api.trello.com/1/member/me/boards?fields=id,name,dateLastView&key=8c1f249e2662ca4952d5df7ea8bad3bc&token=",
            "currentStep[placeInCollection]" : "alphabetical",
            "currentStep[triggerCheck]" : "",
            "currentStep[triggerValue]" : "name",
            "currentStep[thingToRemember]" : "id",
            "currentStep[feedback]" : "Test Feedback",
            "currentStep[nextStepNumber]" : "Test Next Step Number",
            "currentStep[stepState]" : "unfinished",
            "lessonName" : "Test Lesson Name",
            "lessonId" : 1,
            "thirdPartyService" : "trello",
            "originalCount" : False
        }
        response = self.app.post('/check_for_new', data=data, headers=self.headers)
        r = json.loads(response.data)
        
        assert(isinstance(r["original_count"],int))
        assert(r["attribute_to_display"] == False)
        assert(r["attribute_to_remember"] == False)
        assert(r["timeout"] == False)
        assert(r["new_object_added"] == False)

    def test_check_for_new_with_original_count(self):
        response = self.app.post('/signin', data=self.test_user)
        response = json.loads(response.data)
        auth = response["access_token"]
        self.headers = [("Content-Type", "application/x-www-form-urlencoded"),("Authorization", auth)]

        self.test_connection = {
            "service" : "trello",
            "service_access" : "3ad4b59c2f9879726aed00f9ecc3d5a6219d854e4925f44ff5ed53994d424e93"
        }
        self.app.post('/create_connection', data=self.test_connection, headers=self.headers)
        
        data = {
            "currentStep[id]" : 0,
            "currentStep[name]" : "test Step",
            "currentStep[stepType]" : "check_for_new",
            "currentStep[stepNumber]" : 1,
            "currentStep[stepText]" : "Test Step Text",
            "currentStep[triggerEndpoint]" : "https://api.trello.com/1/member/me/boards?fields=id,name,dateLastView&key=8c1f249e2662ca4952d5df7ea8bad3bc&token=",
            "currentStep[placeInCollection]" : "alphabetical",
            "currentStep[triggerCheck]" : "",
            "currentStep[triggerValue]" : "name",
            "currentStep[thingToRemember]" : "id",
            "currentStep[feedback]" : "Test Feedback",
            "currentStep[nextStepNumber]" : "Test Next Step Number",
            "currentStep[stepState]" : "unfinished",
            "lessonName" : "Test Lesson Name",
            "lessonId" : 1,
            "thirdPartyService" : "trello",
            "originalCount" : 1
        }
        response = self.app.post('/check_for_new', data=data, headers=self.headers)
        r = json.loads(response.data)
        
        assert(isinstance(r["original_count"],int))
        assert(r["attribute_to_display"] == "Testing")
        assert(r["attribute_to_remember"] == "52ae697c3ca64bc66a01a4da")
        assert(r["timeout"] == False)
        assert(r["new_object_added"] == True)

if __name__ == '__main__':
    unittest.main()
    