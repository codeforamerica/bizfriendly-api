import unittest, requests
import os, json

class bf_api_tester(unittest.TestCase):
	
	def setUp(self):
		self.api_url = os.environ['API_URL']
		self.currentStep = {
			"triggerEndpoint" : self.api_url+'/api/v1/categories',
			"id" : 1,
			"name" : "Step Test",
			"triggerCheck" : "",
			"triggerValue" : "",
			"stepType" : "test_step",
			"stepNumber" : "1",
			"thingToRemember" : "",
			"nextStepNumber" : "2",
			"feedback" : "<h2>Test Feedback!</h2>",
			"stepText" : "<h1>Test Step Text!</h1>",
			"lessonId" : 1
		},
		self.postData = {
			"currentStep" : self.currentStep,
			"rememberedAttribute" : "Test Attribute",
			"lessonName" : "Test Lesson Name",
			"lessonId" : 1,
			"thirdPartyService" : "bizfriendly_tests",
			"originalCount" : False,
			"originalAttributeValues" : False
		},
		self.headers = {
			"Content-Type" : "multipart/form-data",
			"Authorization" : "b350c70b7ce79ef1c599af65669ec1a24c64513cb9c34c5678df3745d93953d4"
		}

	def test_headers(self):
		r = requests.get(self.api_url+'/api/v1/categories')
		assert(r.headers['Access-Control-Allow-Origin']) == '*'
		assert(r.headers['Content-Type']) == 'application/json'

	def test_categories(self):
		r = requests.get(self.api_url+'/api/v1/categories')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['description'], unicode)
		assert isinstance(response['objects'][0]['url'], unicode)
		assert isinstance(response['objects'][0]['lessons'], list)

	def test_lessons(self):
		r = requests.get(self.api_url+'/api/v1/lessons')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['long_description'], unicode)
		assert isinstance(response['objects'][0]['short_description'], unicode)
		assert isinstance(response['objects'][0]['third_party_service'], unicode)
		assert isinstance(response['objects'][0]['time_estimate'], unicode)
		assert isinstance(response['objects'][0]['difficulty'], unicode)
		assert isinstance(response['objects'][0]['additional_resources'], unicode)
		assert isinstance(response['objects'][0]['tips'], unicode)
		assert isinstance(response['objects'][0]['category_id'], int)
		assert isinstance(response['objects'][0]['category'], dict)

	def test_steps(self):
		r = requests.get(self.api_url+'/api/v1/steps')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['step_type'], unicode)
		assert isinstance(response['objects'][0]['step_number'], unicode)
		assert isinstance(response['objects'][0]['step_text'], unicode)
		assert isinstance(response['objects'][0]['trigger_endpoint'], unicode)
		assert isinstance(response['objects'][0]['trigger_check'], unicode)
		assert isinstance(response['objects'][0]['trigger_value'], unicode)
		assert isinstance(response['objects'][0]['feedback'], unicode)
		assert isinstance(response['objects'][0]['next_step_number'], unicode)
		assert isinstance(response['objects'][0]['thing_to_remember'], unicode)
		assert isinstance(response['objects'][0]['lesson_id'], int)
		assert isinstance(response['objects'][0]['lesson'], dict)

	def test_admin(self):
		r = requests.get(self.api_url+'/api/admin')
		assert(r.headers['content-type']) == 'text/html; charset=utf-8'


	def test_check_for_new(self):
		print "test_check_for_new"
		print json.dumps(self.postData)
		r = requests.post(self.api_url+'/check_for_new', data=json.dumps(self.postData), headers=self.headers)
		response = r.text
		print response

if __name__ == '__main__':
	unittest.main()

































