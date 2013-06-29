import howtocity, unittest, requests, json

class AppTestCase(unittest.TestCase):

	def setUp(self):
		self.app = howtocity.app.test_client()

	def tearDown(self):
		pass

	def test_index(self):
		rv = self.app.get('/')
		
	def test_categories(self):
		rv = self.app.get('/categories')
		assert rv.status_code == 200

	def test_lessons(self):
		rv = self.app.get('/lessons')
		assert rv.status_code == 200

	def test_category(self):
		rv = self.app.get('/promote_your_business_online')
		assert rv.status_code == 200

	def test_lesson(self):
		rv = self.app.get('/promote_your_business_online/facebook_page')
		assert rv.status_code == 200

	def test_instructions(self):
		rv = self.app.get('/promote_your_business_online/facebook_page/instructions/facebook_page_instructions')
		assert rv.status_code == 200

	def test_category_model(self):
		categories = howtocity.Category.query.all()
		assert isinstance(categories, list)
		assert categories[0].id
		assert categories[0].name
		assert categories[0].description
		assert categories[0].url

	def test_lesson_model(self):
		lessons = howtocity.Lesson.query.all()
		assert isinstance(lessons, list)
		assert lessons[0].id
		assert lessons[0].name
		assert lessons[0].description
		assert lessons[0].url
		assert lessons[0].category_id

	# def test_step_model(self):
	# 	steps = app.Step.query.all()
	# 	assert isinstance(steps, list)
	# 	assert steps[0].id
	# 	assert steps[0].name
	# 	assert steps[0].description
	# 	assert steps[0].url
	# 	assert steps[0].category_id

	def test_api_categories(self):
		rv = self.app.get('/api/v1/categories')
		assert rv.status_code == 200
		rv_json = json.loads(rv.data)
		assert isinstance(rv_json['objects'], list)

	def test_api_lessons(self):
		rv = self.app.get('/api/v1/lessons')
		assert rv.status_code == 200
		rv_json = json.loads(rv.data)
		assert isinstance(rv_json['objects'], list)

if __name__ == '__main__':
	unittest.main()