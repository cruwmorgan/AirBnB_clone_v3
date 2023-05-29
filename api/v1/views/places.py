#!/usr/bin/python3
"""new view for Place objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def show_place_by_city_id(city_id):
    """Retrieves the list of all Place objects of a City"""
    req_city = storage.get('City', city_id)
    if req_city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in req_city.places])
    elif request.method == 'POST':
        """Updates a State object"""
        post = request.get_json()
        if post is None or type(post) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        req_obj = City(city_id=city_id, **post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_id(place_id):
    """Retrieves the a Place objects"""
    req_place = storage.get('Place', place_id)
    if req_place is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(req_place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(req_place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(req_place, key, value)
                storage.save()
        return jsonify(req_place.to_dict()), 200
