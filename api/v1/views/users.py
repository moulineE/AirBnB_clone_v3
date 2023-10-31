#!/usr/bin/python3
"""api for users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get all users"""
    allusers = storage.all(User)
    users_list = []
    for user in allusers.values():
        users_list.append(user.to_dict())
    response = jsonify(users_list)
    return response


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    response = jsonify(user.to_dict())
    return response


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    response = jsonify({}), 200
    return response


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, description="Missing password")
    user = User(**request.get_json())
    user.save()
    response = jsonify(user.to_dict()), 201
    return response


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    response = jsonify(user.to_dict()), 200
    return response
