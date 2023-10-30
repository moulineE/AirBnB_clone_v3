#!/usr/bin/python3
"""this module is the flask app"""
from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def SQLsession_close(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
