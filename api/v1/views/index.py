#!/usr/bin/python3
"""the index bluprint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def returns_a_JSON():
    """
    returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_obj():
    """
    retrieves the number of each objects by type
    """
    resp_json = {}
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place", "reviews": "Review", "states": "State",
               "users": "User"}
    for classe in classes:
        resp_json[classe] = storage.count(classes[classe])
    return jsonify(resp_json)
