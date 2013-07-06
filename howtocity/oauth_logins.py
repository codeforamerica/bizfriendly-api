from howtocity import app, db
from flask import request, redirect
import foursquare_lesson

@app.route('/foursquare/login')
def foursquare_login():
	if 'code' in request.args:
		auth_code = request.args['code']
		access_token = foursquare_lesson.get_access_token(auth_code)
		return '{"access_token":"'+access_token+'"}'
	else:
		foursquare_auth_url = foursquare_lesson.foursquare_oauth()
		return redirect(foursquare_auth_url)