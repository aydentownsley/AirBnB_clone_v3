#!/usr/bin/python3
""" sets up status return """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status of API """
    return(jsonify({'status': 'OK'}))
