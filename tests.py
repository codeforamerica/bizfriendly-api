import unittest

from bizfriendly import app
from bizfriendly.models import *
from bizfriendly.routes import *

class bf_api_tester(unittest.TestCase):
    
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hackyourcity@localhost/howtocity'
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.test_user = {
            "name" : "Test User",
            "email" : "TestUserEmail@Tester.com",
            "password" : "Test Password"
        }

    def tearDown(self):
        test_users = Bf_user.query.filter_by(name="Test User").all()
        for test_user in test_users:
            db.session.delete(test_user)
        db.session.commit()

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
        assert isinstance(response['objects'][0]['category_id'], int)
        assert isinstance(response['objects'][0]['lessons'], list)
        assert isinstance(response['objects'][0]['creator_id'], int)

    def test_lessons(self):
        response = self.app.get('/api/v1/lessons')
        response = json.loads(response.data)
        assert isinstance(response, dict)
        assert isinstance(response['objects'], list)
        assert isinstance(response['objects'][0]['id'], int)
        assert isinstance(response['objects'][0]['name'], unicode)
        assert isinstance(response['objects'][0]['description'], unicode)
        assert isinstance(response['objects'][0]['service_id'], int)
        assert isinstance(response['objects'][0]['steps'], list)
        assert isinstance(response['objects'][0]['creator_id'], int)

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
        assert isinstance(response['objects'][0]['trigger_check'], unicode)
        assert isinstance(response['objects'][0]['trigger_value'], unicode)
        assert isinstance(response['objects'][0]['thing_to_remember'], unicode)
        assert isinstance(response['objects'][0]['lesson_id'], int)
        assert isinstance(response['objects'][0]['creator_id'], int)

    # Test Admin --------------------------------

    def test_admin(self):
        response = self.app.get('/api/admin/')
        assert response.headers['content-type'] == 'text/html; charset=utf-8'

    def test_admin_bad_login(self):
        response = self.app.get('/login')
        assert response.headers['content-type'] == 'text/html; charset=utf-8'

    # Test Sign Up and Sign In -------------------

    def test_signup_new_email(self):
        response = self.app.post('/signup', data=self.test_user)
        assert response.status_code == 200 
        response = json.loads(response.data)
        assert "id" in response
        assert "name" in response
        assert response["name"] == "Test User"
        assert "email" in response
        assert "access_token" in response

    def test_signup_same_email(self):
        self.app.post('/signup', data=self.test_user)
        response = self.app.post('/signup', data=self.test_user)
        assert response.status_code == 401
        response = json.loads(response.data)
        assert "error" in response
        assert response["error"] == 'Someone has already signed up with that email.'

    def test_signin(self):
        self.app.post('/signup', data=self.test_user)
        response = self.app.post('/signin', data=self.test_user)
        assert response.status_code == 200 
        response = json.loads(response.data)
        assert "id" in response
        assert "name" in response
        assert response["name"] == "Test User"
        assert "email" in response
        assert "access_token" in response

    def test_signin_bad(self):
        self.app.post('/signup', data=self.test_user)
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
        

    # # def test_check_for_new_no_original_count(self):
    # #     data = {
    # #         "currentStep[id]" : 0,
    # #         "currentStep[name]" : "test Step",
    # #         "currentStep[stepType]" : "check_for_new",
    # #         "currentStep[stepNumber]" : 1,
    # #         "currentStep[stepText]" : "Test Step Text",
    # #         "currentStep[triggerEndpoint]" : "https://graph.facebook.com/me/accounts?fields=name&access_token=",
    # #         "currentStep[triggerCheck]" : "data",
    # #         "currentStep[triggerValue]" : "name",
    # #         "currentStep[thingToRemember]" : "Test Thing to remember",
    # #         "currentStep[feedback]" : "Test Feedback",
    # #         "currentStep[nextStepNumber]" : "Test Next Step Number",
    # #         "currentStep[stepState]" : "unfinished",
    # #         "lessonName" : "Test Lesson Name",
    # #         "lessonId" : 0,
    # #         "thirdPartyService" : "facebook",
    # #         "originalCount" : False
    # #     }
    # #     if self.env == 'local':
    # #         headers = {
    # #             "authorization" : "30210c670811c191ea2286632682cdcc18566a4892462bb98a1c603f56d22150"
    # #         }
    # #     if self.env == 'staging':
    # #         headers = {
    # #             "authorization" : "15c76cdaa958ca537146395d612fbd2fdc52f181e852c1ba7943f8cd72c36f8f"
    # #         }
    # #     if self.env == 'production':
    # #         headers = {
    # #             "authorization" : "0dd9def6a8a5db75a22e7d83adf9a46e8829c6da6f64c7516dc797ba64506228"
    # #         }
    # #     bizfriendly_url = self.api_url[0:-4] #trim off '/api'
    # #     r = requests.post(bizfriendly_url+'/check_for_new', data=data, headers=headers)
    # #     r = r.json()
    # #     # {u'original_count': 207, u'attribute_to_display': False, u'attribute_to_remember': False, u'timeout': False, u'new_object_added': False}
    # #     assert(isinstance(r["original_count"],int))
    # #     assert(r["attribute_to_display"] == False)
    # #     assert(r["attribute_to_remember"] == False)
    # #     assert(r["timeout"] == False)
    # #     assert(r["new_object_added"] == False)

    # # def test_check_for_new_with_original_count(self):
    # #     data = {
    # #         "currentStep[id]" : 0,
    # #         "currentStep[name]" : "test Step",
    # #         "currentStep[stepType]" : "check_for_new",
    # #         "currentStep[stepNumber]" : 1,
    # #         "currentStep[stepText]" : "Test Step Text",
    # #         "currentStep[triggerEndpoint]" : "https://graph.facebook.com/me/accounts?fields=name&access_token=",
    # #         "currentStep[triggerCheck]" : "data",
    # #         "currentStep[triggerValue]" : "name",
    # #         "currentStep[thingToRemember]" : "id",
    # #         "currentStep[feedback]" : "Test Feedback",
    # #         "currentStep[nextStepNumber]" : "Test Next Step Number",
    # #         "currentStep[stepState]" : "unfinished",
    # #         "lessonName" : "Test Lesson Name",
    # #         "lessonId" : 0,
    # #         "thirdPartyService" : "facebook",
    # #         "originalCount" : 1
    # #     }
    # #     if self.env == 'local':
    # #         headers = {
    # #             "authorization" : "30210c670811c191ea2286632682cdcc18566a4892462bb98a1c603f56d22150"
    # #         }
    # #     if self.env == 'staging':
    # #         headers = {
    # #             "authorization" : "15c76cdaa958ca537146395d612fbd2fdc52f181e852c1ba7943f8cd72c36f8f"
    # #         }
    # #     if self.env == 'production':
    # #         headers = {
    # #             "authorization" : "0dd9def6a8a5db75a22e7d83adf9a46e8829c6da6f64c7516dc797ba64506228"
    # #         }
    # #     bizfriendly_url = self.api_url[0:-4] #trim off '/api'
    # #     r = requests.post(bizfriendly_url+'/check_for_new', data=data, headers=headers)
    # #     r = r.json()
    # #     # {u'original_count': 207, u'attribute_to_display': False, u'attribute_to_remember': False, u'timeout': False, u'new_object_added': False}
    # #     assert(isinstance(r["original_count"],int))
    # #     assert(isinstance(r["attribute_to_display"],unicode))
    # #     assert(isinstance(r["attribute_to_remember"],unicode))
    # #     assert(r["timeout"] == False)
    # #     assert(r["new_object_added"] == True)

    # def test_post_existing_category(self):
    #     data = {
    #         "name" : "Test Category",
    #         "description" : "Test Description",
    #         "state" : "Test State"
    #     }
    #     headers = {
    #         'Content-Type' : 'application/json'
    #     }
    #     r = requests.post(self.api_url+'/v1/categories', data=json.dumps(data), headers=headers)
    #     assert(r.status_code == 400)

    # def test_put_existing_category(self):
    #     def random_char(num):
    #         return ''.join(choice(ascii_lowercase) for x in range(num))
    #     data = {
    #         "name" : "Test Category",
    #         "description" : random_char(10),
    #         "state" : "Test State"
    #     }
    #     headers = {
    #         'Content-Type' : 'application/json'
    #     }
    #     r = requests.get(self.api_url+'/v1/categories')
    #     response = r.json()
    #     test_category_id = 0
    #     for category in response['objects']:
    #         if category["name"] == "Test Category":
    #             test_category_id = str(category["id"])

    #     r = requests.put(self.api_url+'/v1/categories/'+test_category_id, data=json.dumps(data), headers=headers)
    #     assert(r.status_code == 200)

    # def test_new_content_email(self):
    #     newCategory = {
    #       "name" : "Testing New Skill",
    #       "description" : "Testing new skill description.",
    #       "state" : "draft",
    #       "creator_id" : 1
    #     }
    #     bizfriendly_url = self.api_url[0:-4] #trim off '/api'
    #     r = requests.post(bizfriendly_url+"/new_content_email", newCategory)
    #     r = r.json()
    #     assert r["message"] == "Queued. Thank you."

if __name__ == '__main__':
    unittest.main()