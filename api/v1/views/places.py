#!/usr/bin/python3
"""api for places"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    response = jsonify(places_list)
    return response


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    response = jsonify(place.to_dict())
    return response


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    response = jsonify({}, status=200)
    return response


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    response = jsonify(place.to_dict(), status=201)
    return response


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    response = jsonify(place.to_dict(), status=200)
    return response
