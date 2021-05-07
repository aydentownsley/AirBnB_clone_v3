#!/usr/bin/python3
""" sets up status return """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status of API """
    return(jsonify({'status': 'OK'}))


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrives the number of each obj by class"""
    obj_dict = {}
    for k, v in classes.items():
        obj_dict[k] = storage.count(v)
    return jsonify(obj_dict)

if __name__ == "__main__":
    pass
