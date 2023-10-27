#!/usr/bin/python3
"""State view"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """retrieves the list of all State object"""
    states = storage.all(State)
    return [state.to_dict() for state in states.values()]


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    data = request.get_json()
    if type(data) != dict:
        abort(400, {'message': 'Not a JSON'})
    if 'name' not in data:
        return abort(400, {'message': 'Missing name'})
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a State object"""
    ignored_keys = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if type(data) != dict:
            return abort(400, {'message': 'Not a JSON'})
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
