#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def show_by_id(state_id):
    """Retrieves the list of all City objects of a State"""
    req_state = storage.get('State', state_id)
    if req_state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in req_state.cities])
    elif request.method == 'POST':
        """Updates a State object"""
        post = request.get_json()
        if post is None or type(post) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        req_obj = City(state_id=state_id, **post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city_list(city_id):
    """Retrieves the list of all City objects"""
    req_city = storage.get('City', city_id)
    if req_city is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(req_city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(req_city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(req_city, key, value)
                storage.save()
        return jsonify(req_city.to_dict()), 200
