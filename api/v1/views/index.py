#!/usr/bin/python3
"""the index bluprint"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def returns_a_JSON():
    """
    returns a JSON: "status": "OK"
    """
    return {'status': 'OK'}
