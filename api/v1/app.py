#!/usr/bin/python3
""" Flask App """
from models import storage
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flasgger.utils import swag_from
from flask_cors import CORS
from flasgger import Swagger
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ end Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 
    Error 404
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ main """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
