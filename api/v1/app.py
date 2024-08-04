#!/usr/bin/python3
"""handling API requests"""

from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

CORS(app, origins="0.0.0.0")

api_host = getenv("HBNB_API_HOST", "0.0.0.0")
api_port = getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown(self):
    """Closing the db storage connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handling 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=api_host, port=int(api_port), threaded=True)
