#!/usr/bin/python3
"""User view"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """creates a User object"""
    try:
        data = request.get_json()
        if 'email' not in data:
            raise KeyError('Missing email')
        if 'password' not in data:
            raise KeyError('Missing password')
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    except KeyError as error:
        abort(400, description=error.args[0])
    except Exception:
        abort(400, description='Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates a User object"""
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    except Exception:
        abort(400, description='Not a JSON')
