#!/usr/bin/python3
""" creating api view for states objs """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_of_state(state_id):
    """ retrieves list of all city objs of spec State """
    cities_list = []
    s_id = storage.get(State, state_id)
    if not s_id:
        abort(404)
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return make_response(jsonify(cities_list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves one single city object """
    c_id = storage.get(City, city_id)
    if not c_id:
        abort(404)
    return make_response(jsonify(c_id.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """ deletes one single city object """
    c_id = storage.get(City, city_id)
    if not c_id:
        abort(404)
    storage.delete(c_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ creates one single city object """
    s_id = storage.get(State, state_id)
    if not s_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': "Missing name"}), 400)
    content = request.get_json()
    new_city = City()
    new_city.name = content['name']
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>/', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates one single state object """
    c_id = storage.get(City, city_id)
    if not c_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if k in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(c_id, k, v)
    storage.save()
    return make_response(jsonify(c_id.to_dict()), 200)
