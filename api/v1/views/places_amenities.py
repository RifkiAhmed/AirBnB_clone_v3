#!/usr/bin/python3
"""view between Place and Amenity objects"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route(
        '/places/<place_id>/amenities', strict_slashes=False, methods=['GET'])
def get_place_amenities(place_id):
    """retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """deletes a place Amenity object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity and amenity in place.amenities:
        if storage_t == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenities_id.remove(amenity.id)
        place.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)
