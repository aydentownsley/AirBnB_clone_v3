#!/usr/bin/python3
"""Create a route for places"""
from os import getenv
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_by_city(city_id):
    """Display list of places by a given city"""
    c_id = storage.get(City, city_id)
    if c_id is None:
        abort(404)
    places_list = []
    all_places = storage.all(Place).values()
    for place in all_places:
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Display the place by place_id"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    return make_response(jsonify(p_id.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Deletes a Place by place_id"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    storage.delete(p_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates one single Place object given City"""
    c_id = storage.get(City, city_id)
    if not c_id:
        abort(404)
    place_req = request.get_json()
    if not place_req:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    u_id = storage.get(User, place_req['user_id'])
    if not u_id:
        abort(404)
    if "name" not in place_req():
        return make_response(jsonify({'error': "Missing name"}), 400)
    content = request.get_json()
    new_place = Place()
    new_place.name = content['name']
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates one single place object"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if k in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(p_id, k, v)
    storage.save()
    return jsonify(p_id.to_dict()), 200
