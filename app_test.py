import app, unittest

class AppTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def test_index(self):
		rv = self.app.get('/')
		
	def test_categories(self):
		rv = self.app.get('/categories')
		assert rv.status_code == 200

	def test_category(self):
		rv = self.app.get('/category/promote_your_business_online')
		assert rv.status_code == 200

	def test_lesson(self):
		rv = self.app.get('/category/promote_your_business_online/lesson/facebook_page')
		assert rv.status_code == 200

	def test_instructions(self):
		rv = self.app.get('/category/promote_your_business_online/lesson/facebook_page/facebook_page_instructions')
		assert rv.status_code == 200

	def test_category_model(self):
		categories = app.Category.query.all()
		assert isinstance(categories, list)
		assert categories[0].id
		assert categories[0].name
		assert categories[0].description
		assert categories[0].url

	def test_lesson_model(self):
		lessons = app.Lesson.query.all()
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


if __name__ == '__main__':
	unittest.main()