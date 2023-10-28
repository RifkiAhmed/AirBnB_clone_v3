#!/usr/bin/python3
"""Review view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.review import Review
from models.user import User
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


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """creates a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if 'user_id' not in data:
            raise KeyError('Missing user_id')
        user = storage.get(User, data.get('user_id'))
        if not user:
            raise ValueError
        if 'text' not in data:
            raise KeyError('Missing text')
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)
    except KeyError as error:
        abort(400, description=error.args[0])
    except ValueError:
        abort(404)
    except Exception:
        abort(400, description='Not a JSON')
