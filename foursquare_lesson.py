import foursquare, sys, logging
from flask import render_template, request
loghandler = logging.StreamHandler(stream=sys.stdout)
foursquare.log.addHandler(loghandler)
foursquare.log.setLevel(logging.DEBUG)

client_id = 'IRVYNL0DUD5HDFNSCPPFU1PPERAZSVHBVTTRUUF2AA5EPB1A'
client_secret = '4B0NEIC2YBADH4HHDELEABVIEDJXN4YJYZ2KCOSXXKDYH0BT'
redirect_uri = 'http://0.0.0.0:5000/promote_your_business_online/foursquare/instructions/foursquare_instructions'

def foursquare_oauth():
	# Construct the client object
	client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	# Build the authorization url for your app
	foursquare_auth_url = client.oauth.auth_url()
	return foursquare_auth_url

def get_access_token(auth_code):
	# Construct the client object
	client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	# Interrogate foursquare's servers to get the user's access_token
	access_token = client.oauth.get_token(auth_code)
	return access_token
	
def get_user_data(access_token):
	# Construct the client object
	client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	# Apply the returned access token to the client
	client.set_access_token(access_token)
	# Get the user's data
	user = client.users()
	return user

def venue_api(venue_id):
	client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	venue = client.venues(venue_id)
	return venue