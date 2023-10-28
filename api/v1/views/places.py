#!/usr/bin/python3
"""Place view"""
from api.v1.views import app_views
from flask import abort, jsonify
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
