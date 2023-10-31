#!/usr/bin/python3
"""api for places reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    response = jsonify(reviews_list)
    return response


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    response = jsonify(review.to_dict())
    return response


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    response = jsonify({}, status=200)
    return response


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "text" not in request.get_json():
        abort(400, description="Missing text")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    response = jsonify(review.to_dict(), status=201)
    return response


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    response = jsonify(review.to_dict(), status=200)
    return response
