#!/usr/bin/python3
"""api for amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities_list():
    """get amenities"""
    amenities_list = []
    amenities = storage.all(Amenity)
    if amenities is None:
        return abort(404)
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete an amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    response = jsonify({}), 200
    return response


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """create an amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    response = jsonify(amenity.to_dict()), 201
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    response = jsonify(amenity.to_dict()), 200
    return response
