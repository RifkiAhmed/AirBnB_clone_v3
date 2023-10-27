#!/usr/bin/python3
"""Flask web application"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(_):
    """remove the current SQLAlchely after each request"""
    storage.close()


if __name__ == "__main__":
    from os import getenv
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
