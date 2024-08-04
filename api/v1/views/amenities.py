#!/usr/bin/python3
"""API Routes
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_amenities():
    """Retrieving all amenities
    """
    amenities = storage.all("Amenity")
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """Retrieving an amenity by ID
    """
    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deleting an amenity
    """
    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """Creating amenity
    """
    amenity_data = request.get_json(force=True, silent=True)
    if type(amenity_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in amenity_data:
        amenity = classes["Amenity"](**amenity_data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def put_amenity(amenity_id):
    """Updating amenity
    """
    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)

    amenity_data = request.get_json(force=True, silent=True)
    if type(amenity_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in amenity_data.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
