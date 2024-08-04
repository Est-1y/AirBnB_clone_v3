#!/usr/bin/python3
"""API Routes """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("states/<state_id>/cities",
                 strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    """Retrieving cities for states"""
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Retrieving a city by ID"""
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    """Deleting a city"""
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def post_city(state_id):
    """Creating a new city"""
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    city_data = request.get_json(force=True, silent=True)
    if type(city_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in city_data:
        city = classes["City"](state_id=state_id, **city_data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id):
    """Updating city"""
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    city_data = request.get_json(force=True, silent=True)
    if type(city_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in city_data.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
