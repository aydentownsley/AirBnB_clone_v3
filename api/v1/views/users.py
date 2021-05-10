#!/usr/bin/python3
""" creating api view for states objs """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ retrieves list of all users """
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return make_response(jsonify(users_list), 200)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ retrieves one single user object """
    u_id = storage.get(User, user_id)
    if not u_id:
        abort(404)
    return make_response(jsonify(u_id.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """ deletes one single user object """
    u_id = storage.get(User, user_id)
    if not u_id:
        abort(404)
    storage.delete(u_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creates one single user object """
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': "Missing password"}), 400)
    content = request.get_json()
    new_user = User()
    new_user.email = content['email']
    new_user.password = content['password']
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates one single state object """
    u_id = storage.get(User, user_id)
    if not u_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if k in ['id', 'email', 'created_at', 'updated_at']:
            pass
        else:
            setattr(u_id, k, v)
    storage.save()
    return make_response(jsonify(u_id.to_dict()), 200)
