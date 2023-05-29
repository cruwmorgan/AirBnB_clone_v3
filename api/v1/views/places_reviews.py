#!/usr/bin/python3
"""new view for Review objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def show_review_by_place_id(place_id):
    """Retrieves the list of all Review objects of a Place"""
    req_place = storage.get('Place', place_id)
    if req_place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in req_place.reviews])
    elif request.method == 'POST':
        """Updates a Review object"""
        post = request.get_json()
        if post is None or type(post) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)
        elif post.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400
        req_obj = Review(place_id=place_id, **post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_by_id(review_id):
    """Retrieves the a Place objects"""
    req_rev = storage.get('Review', review_id)
    if req_rev is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(req_rev.to_dict())
    elif request.method == 'DELETE':
        storage.delete(req_rev)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(req_rev, key, value)
                storage.save()
        return jsonify(req_rev.to_dict()), 200
