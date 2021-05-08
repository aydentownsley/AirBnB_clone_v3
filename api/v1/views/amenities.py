#!/usr/bin/python3
"""Create a route for amenities"""
from os import getenv
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Display all amenities"""
    ame_dict = []
    for obj in storage.all(Amenity).values():
        ame_dict.append(obj.to_dict())
    return make_response(jsonify(ame_dict), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_ameid(amenity_id):
    """Display amenities by amenity_id"""
    ame_id = storage.get(Amenity, amenity_id)
    if ame_id is not None:
        return make_response(jsonify(ame_id.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete amentiy by amenity_id"""
    ame_id = storage.get(Amenity, amenity_id)
    if ame_id is not None:
        storage.delete(ame_id)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new Amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': "Missing name"}), 400)
    content = request.get_json()
    new_ame = Amenity()
    new_ame.name = content['name']
    new_ame.save()
    return make_response(jsonify(new_ame.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update a Amenity object by amenity_id"""
    ame_id = storage.get(Amenity, amenity_id)
    if not ame_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    content = request.get_json()
    for key, val in request.get_json().items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(ame_id, key, val)
    storage.save()
    return make_response(jsonify(ame_id.to_dict()), 200)
