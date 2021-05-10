#!/usr/bin/python3
""" Starts Flask web app """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """ closes storage on teardown """
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns page not found 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
