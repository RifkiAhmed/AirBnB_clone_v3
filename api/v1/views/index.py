#!/usr/bin/python3
"""Index html"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """return response status code"""
    return jsonify({'status': 'OK'})
