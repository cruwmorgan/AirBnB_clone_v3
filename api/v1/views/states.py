#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        m_list = []
        for obj in storage.all(State).values():
            m_list.append(obj.to_dict())
        return jsonify(m_list)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        req_obj = State(**post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def show_by_state_id(state_id):
    """Retrieves a State object by id"""
    req_state = storage.get('State', state_id)
    if req_state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(req_state.to_dict())
    elif request.method == 'DELETE':
        req_state = storage.get('State', state_id)
        storage.delete(req_state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        """Updates a State object"""
        put = request.get_json()
        if put is None or type(put) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(req_state, key, value)
                storage.save()
        return jsonify(req_state.to_dict()), 200
