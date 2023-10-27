#!/usr/bin/python3
"""State view"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """retrieves the list of all State object"""
    states = storage.all(State)
    return [state.to_dict() for state in states.values()]


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return state.to_dict()
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """deletes a State object"""
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        return make_response(jsonify({}), 200)
    else:
        abort(404)
