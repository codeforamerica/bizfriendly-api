if [ ! -f .venv/.Python ]; 
	then
	virtualenv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

# Uncomment and point towards your local postgres db.
export DATABASE_URL='postgres://hackyourcity@localhost/howtocity'

# Uncomment and set secret key to whatever unique value you want.
export SECRET_KEY='123456'
export API_URL='http://app.bizfriend.ly'
# export API_URL='http://app.bizfriend.ly/api'
# export API_URL='http://app-staging.bizfriend.ly/api'
# export API_URL='http://127.0.0.1:8000/api'
export ENV="local"
