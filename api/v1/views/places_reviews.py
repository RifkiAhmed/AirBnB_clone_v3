#!/usr/bin/python3
"""Review view"""
from api.v1.views import app_views
from flask import abort, jsonify
from models.place import Place
from models.review import Review
from models import storage


@app_views.route(
        '/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)
