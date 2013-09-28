from flask import Flask

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

import config, admin, routes, api