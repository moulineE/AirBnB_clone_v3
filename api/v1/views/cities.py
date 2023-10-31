#!/usr/bin/python3
"""api for cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """get states cities"""
    cites_list = []
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    for city in state.cities:
        cites_list.append(city.to_dict())
    return jsonify(cites_list)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get states cities"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    response = jsonify({}), 200
    return response


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    response = jsonify(city.to_dict()), 201
    return response


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a state"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    response = jsonify(city.to_dict()), 200
    return response
