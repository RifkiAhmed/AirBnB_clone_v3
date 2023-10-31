#!/usr/bin/python3
"""Place view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route(
        '/places_search', strict_slashes=False, methods=['POST'])
def places_search():
    """retrieves all Place objects depending of the JSON in the request body"""
    try:
        data = request.get_json()
        if not data or not (
                data.get('states')
                or data.get('cities')
                or data.get('amenities')):
            places = storage.all(Place)
            return jsonify([place.to_dict() for place in places])
        cities = []
        places = []
        if data.get('states'):
            for state_id in data.get('states'):
                state = storage.get(State, state_id)
            if state:
                cities += state.cities
        if data.get('cities'):
            for city_id in data.get('cities'):
                city = storage.get(City, city_id)
                if city and city not in cities:
                    cities.append(city)
        if cities:
            for city in cities:
                places += city.places
        else:
            places = storage.all(Place)
        places_filtred = []
        if data.get('amenities'):
            for place in places:
                for amenity in place.amenities:
                    if amenity.id in data.get('amenities'):
                        places_filtred.append(place)
            return jsonify([place.to_dict() for place in places.filtred])
        else:
            return jsonify([place.to_dict() for place in places])
    except Exception:
        abort(400, description='Not a JSON')


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


@app_views.route(
        '/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if 'user_id' not in data:
            raise KeyError('Missing user_id')
        user = storage.get(User, data.get('user_id'))
        if not user:
            raise ValueError
        if 'name' not in data:
            raise KeyError('Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
    except KeyError as error:
        abort(400, description=error.args[0])
    except ValueError:
        abort(404)
    except Exception:
        abort(400, description='Not a JSON')


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a Place object"""
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    except Exception:
        abort(400, description='Not a JSON')
