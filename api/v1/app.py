#!/usr/bin/python3
"""this module is the flask app"""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
from flask import jsonify
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def SQLsession_close(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler
     a handler for 404 errors that
     returns a JSON-formatted
     404 status code response
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
