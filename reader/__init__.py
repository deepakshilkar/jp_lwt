from flask import Flask

reader = Flask(__name__)

from reader import routes
