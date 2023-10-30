#!/usr/bin/python3
"""api for states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_states():
    """get all states"""
    allstates = storage.all(State)
    states_list = []
    for state in allstates.values():
        states_list.append(state.to_dict())
    response = jsonify(states_list)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """get a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    response = jsonify(state.to_dict())
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    response = jsonify({})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/states/', methods=['POST'])
def create_state():
    """create a state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    state = State(**request.get_json())
    state.save()
    response = jsonify(state.to_dict())
    response.status_code = 201
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    response = jsonify(state.to_dict())
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response
