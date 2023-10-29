#!/usr/bin/python3
"""view between Place and Amenity objects"""
from api.v1.views import app_views
from flask import abort, jsonify
from models.place import Place
from models.amenity import Amenity
from models import storage


@app_views.route(
        '/places/<place_id>/amenities', strict_slashes=False, methods=['GET'])
def get_places_amenities(place_id):
    """retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        abort(404)
