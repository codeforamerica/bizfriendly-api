import unittest, requests, os, json

class bf_api_tester(unittest.TestCase):
	
	def setUp(self):
		self.api_url = os.environ['API_URL']
		self.env = os.environ['ENV']

	def test_headers(self):
		r = requests.get(self.api_url+'/v1/categories')
		assert(r.headers['Access-Control-Allow-Origin']) == '*'
		assert(r.headers['Content-Type']) == 'application/json'

	def test_categories(self):
		r = requests.get(self.api_url+'/v1/categories')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['description'], unicode)
		assert isinstance(response['objects'][0]['url'], unicode)
		assert isinstance(response['objects'][0]['state'], unicode)
		assert isinstance(response['objects'][0]['services'], list)
		assert isinstance(response['objects'][0]['creator_id'], int)

	def test_services(self):
		r = requests.get(self.api_url+'/v1/services')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['long_description'], unicode)
		assert isinstance(response['objects'][0]['short_description'], unicode)
		assert isinstance(response['objects'][0]['additional_resources'], unicode)
		assert isinstance(response['objects'][0]['tips'], unicode)
		assert isinstance(response['objects'][0]['category_id'], int)
		assert isinstance(response['objects'][0]['lessons'], list)
		assert isinstance(response['objects'][0]['creator_id'], int)

	def test_lessons(self):
		r = requests.get(self.api_url+'/v1/lessons')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['description'], unicode)
		assert isinstance(response['objects'][0]['service_id'], int)
		assert isinstance(response['objects'][0]['steps'], list)
		assert isinstance(response['objects'][0]['creator_id'], int)


	def test_steps(self):
		r = requests.get(self.api_url+'/v1/steps')
		response = r.json()
		assert isinstance(response, dict)
		assert isinstance(response['objects'], list)
		assert isinstance(response['objects'][0]['id'], int)
		assert isinstance(response['objects'][0]['name'], unicode)
		assert isinstance(response['objects'][0]['step_type'], unicode)
		assert isinstance(response['objects'][0]['step_number'], int)
		assert isinstance(response['objects'][0]['step_text'], unicode)
		assert isinstance(response['objects'][0]['trigger_endpoint'], unicode)
		assert isinstance(response['objects'][0]['trigger_check'], unicode)
		assert isinstance(response['objects'][0]['trigger_value'], unicode)
		assert isinstance(response['objects'][0]['thing_to_remember'], unicode)
		assert isinstance(response['objects'][0]['feedback'], unicode)
		assert isinstance(response['objects'][0]['lesson_id'], int)
		assert isinstance(response['objects'][0]['creator_id'], int)

	def test_admin(self):
		r = requests.get(self.api_url+'/admin')
		assert(r.headers['content-type']) == 'text/html; charset=utf-8'

	def test_check_for_new_no_original_count(self):
		data = {
			"currentStep[id]" : 0,
			"currentStep[name]" : "test Step",
			"currentStep[stepType]" : "check_for_new",
			"currentStep[stepNumber]" : 1,
			"currentStep[stepText]" : "Test Step Text",
			"currentStep[triggerEndpoint]" : "https://graph.facebook.com/me/accounts?fields=name&access_token=",
			"currentStep[triggerCheck]" : "data",
			"currentStep[triggerValue]" : "name",
			"currentStep[thingToRemember]" : "Test Thing to remember",
			"currentStep[feedback]" : "Test Feedback",
			"currentStep[nextStepNumber]" : "Test Next Step Number",
			"currentStep[stepState]" : "unfinished",
			"lessonName" : "Test Lesson Name",
			"lessonId" : 0,
			"thirdPartyService" : "facebook",
			"originalCount" : False
		}
		if self.env == 'local':
			headers = {
				"authorization" : "30210c670811c191ea2286632682cdcc18566a4892462bb98a1c603f56d22150"
			}
		if self.env == 'staging':
			headers = {
				"authorization" : "15c76cdaa958ca537146395d612fbd2fdc52f181e852c1ba7943f8cd72c36f8f"
			}
		if self.env == 'production':
			headers = {
				"authorization" : "0dd9def6a8a5db75a22e7d83adf9a46e8829c6da6f64c7516dc797ba64506228"
			}
		bizfriendly_url = self.api_url[0:-4] #trim off '/api'
		r = requests.post(bizfriendly_url+'/check_for_new', data=data, headers=headers)
		r = r.json()
		# {u'original_count': 207, u'attribute_to_display': False, u'attribute_to_remember': False, u'timeout': False, u'new_object_added': False}
		assert(isinstance(r["original_count"],int))
		assert(r["attribute_to_display"] == False)
		assert(r["attribute_to_remember"] == False)
		assert(r["timeout"] == False)
		assert(r["new_object_added"] == False)

	def test_check_for_new_with_original_count(self):
		data = {
			"currentStep[id]" : 0,
			"currentStep[name]" : "test Step",
			"currentStep[stepType]" : "check_for_new",
			"currentStep[stepNumber]" : 1,
			"currentStep[stepText]" : "Test Step Text",
			"currentStep[triggerEndpoint]" : "https://graph.facebook.com/me/accounts?fields=name&access_token=",
			"currentStep[triggerCheck]" : "data",
			"currentStep[triggerValue]" : "name",
			"currentStep[thingToRemember]" : "id",
			"currentStep[feedback]" : "Test Feedback",
			"currentStep[nextStepNumber]" : "Test Next Step Number",
			"currentStep[stepState]" : "unfinished",
			"lessonName" : "Test Lesson Name",
			"lessonId" : 0,
			"thirdPartyService" : "facebook",
			"originalCount" : 1
		}
		if self.env == 'local':
			headers = {
				"authorization" : "30210c670811c191ea2286632682cdcc18566a4892462bb98a1c603f56d22150"
			}
		if self.env == 'staging':
			headers = {
				"authorization" : "15c76cdaa958ca537146395d612fbd2fdc52f181e852c1ba7943f8cd72c36f8f"
			}
		if self.env == 'production':
			headers = {
				"authorization" : "0dd9def6a8a5db75a22e7d83adf9a46e8829c6da6f64c7516dc797ba64506228"
			}
		bizfriendly_url = self.api_url[0:-4] #trim off '/api'
		r = requests.post(bizfriendly_url+'/check_for_new', data=data, headers=headers)
		r = r.json()
		# {u'original_count': 207, u'attribute_to_display': False, u'attribute_to_remember': False, u'timeout': False, u'new_object_added': False}
		assert(isinstance(r["original_count"],int))
		assert(isinstance(r["attribute_to_display"],unicode))
		assert(isinstance(r["attribute_to_remember"],unicode))
		assert(r["timeout"] == False)
		assert(r["new_object_added"] == True)

if __name__ == '__main__':
	unittest.main()






















