#!/usr/bin/python3
"""Create a route for reviews"""
from os import getenv
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_by_place(place_id):
    """Display list of reviews from a spec place"""
    p_id = storage.get(Place, place_id)
    if p_id is None:
        abort(404)
    reviews_list = []
    all_reviews = storage.all(Review).values()
    for review in all_reviews:
        if reviews.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates one single review given spec place"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    review_req = request.get_json()
    if not review_req:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if "user_id" not in review_req:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    u_id = storage.get(User, review_req['user_id'])
    if not u_id:
        abort(404)
    if "text" not in review_req:
        return make_response(jsonify({'error': "Missing name"}), 400)
    new_review = Review()
    new_review.user_id = review_req['user_id']
    new_review.place_id = p_id
    new_review.text = review_req['text']
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates one single review object"""
    r_id = storage.get(Review, review_id)
    if not r_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if k in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(r_id, k, v)
    storage.save()
    return jsonify(r_id.to_dict()), 200
