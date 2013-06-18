if [ ! -f venv/.Python ]; 
	then
	virtualenv venv
fi

source venv/bin/activate
pip install -r requirements.txt