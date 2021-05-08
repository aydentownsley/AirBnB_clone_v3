#!/usr/bin/python3
""" creating api view for states objs """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ retrieves list of all state objs """
    states_list = []
    for state in storage.all(State).values():
        state_dict = state.to_dict()
        states_list.append(state_dict)
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ retrieves one single state object """
    s_id = storage.get(State, state_id)
    if not s_id:
        abort(404)
    return make_response(jsonify(s_id.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """ deletes one single state object """
    s_id = storage.get(State, state_id)
    if not s_id:
        abort(404)
    storage.delete(s_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates one single state object """
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': "Missing name"}), 400)
    content = request.get_json()
    new_state = State()
    new_state.name = content['name']
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates one single state object """
    s_id = storage.get(State, state_id)
    if not s_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if k in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(s_id, k, v)
    storage.save()
    return make_response(jsonify(s_id.to_dict()), 200)
