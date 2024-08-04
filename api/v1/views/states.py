#!/usr/bin/python3
"""API Routes"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """Retrieving all states"""
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Retrieving a state by ID"""
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Deleting a state"""
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states/", strict_slashes=False, methods=["POST"])
def post_state():
    """Creating state"""
    state_data = request.get_json(force=True, silent=True)
    if type(state_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in state_data:
        new_state = classes["State"](**state_data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id):
    """Updating state"""
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    data_json = request.get_json(force=True, silent=True)
    if type(data_json) is not dict:
        abort(400, "Not a JSON")

    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict())
