"""
BizFriendly is setup as a contained python module.
This file creates the Flask app then imports the other parts of the module.
"""
from flask import Flask

app = Flask(__name__)

import settings, admin, routes, api
