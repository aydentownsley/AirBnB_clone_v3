#!/usr/bin/python3
"""Create a route for new view for the link between Place objects
and Amenity objects that handles all default RestFul API actions"""
from os import getenv
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
using_storage = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    p_id = storage.get(Place, place_id)
    if p_id is None:
        abort(404)
    ame_list = []
    for p_id in p_id.amenities:
        ame_list.append(p_id.to_dict())
    return jsonify(ame_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_ame_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    a_id = storage.get(Amenity, amenity_id)
    if not a_id:
        abort(404)
    if a_id not in p_id.amenities:
        abort(404)
    storage.delete(a_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_ame_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    a_id = storage.get(Amenity, amenity_id)
    if not a_id:
        abort(404)
    if a_id in p_id.amenities:
        return make_response(jsonify(a_id.to_dict(), 200))
    return make_response(jsonify(a_id.to_dict(), 201))
