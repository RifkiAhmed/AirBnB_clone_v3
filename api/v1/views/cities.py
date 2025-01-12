#!/usr/bin/python3
"""State view"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from models.state import State
from models.city import City
from models import storage


@app_views.route(
        '/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """retrieves the list of all cities related to a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """creates a new City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
        if 'name' not in data:
            raise KeyError
        data["state_id"] = state_id
        city = City(**data)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)
    except KeyError:
        abort(400, description='Missing name')
    except Exception:
        abort(400, description='Not a JSON')


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates a City object"""
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    except Exception:
        abort(400, description='Not a JSON')
