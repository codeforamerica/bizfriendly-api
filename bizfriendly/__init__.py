from flask import Flask

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

import config, api, admin, routes