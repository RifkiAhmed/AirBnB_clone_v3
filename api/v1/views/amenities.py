#!/usr/bin/python3
"""Amenity view"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """creates an Amenity object"""
    try:
        data = request.get_json()
        if 'name' not in data:
            raise KeyError
        amenity = Amenity(**data)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    except KeyError:
        abort(400, description='Missing name')
    except Exception:
        abort(400, description='Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """updates an Amenity object"""
    ignored_keys = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    except Exception:
        abort(400, description='Not a JSON')
