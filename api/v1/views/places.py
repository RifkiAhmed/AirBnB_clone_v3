#!/usr/bin/python3
"""Place view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response
from models.place import Place
from models.city import City
from models import storage


@app_views.route(
        '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """retrieves the list of all Place objects related to a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)
