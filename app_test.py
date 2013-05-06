import app, unittest

class AppTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def test_index(self):
		rv = self.app.get('/')
		assert '200 OK' in rv.status
		assert '<script src="/static/js/index.js"></script>' in rv.data

	def test_fb(self):
		rv = self.app.get('/fb_page_instructions.html')
		assert '200 OK' in rv.status
		assert '<script src="/static/js/facebook_page.js"></script>' in rv.data


if __name__ == '__main__':
	unittest.main()