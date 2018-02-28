from flask import Flask
from flask_restful import Api

reader = Flask(__name__)

from reader import routes
