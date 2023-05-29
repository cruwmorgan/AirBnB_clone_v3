#!/usr/bin/python3
"""new view for User objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def user_list():
    """Retrieves the list of all User objects"""
    if request.method == 'GET':
        m_list = []
        for obj in storage.all(User).values():
            m_list.append(obj.to_dict())
        return jsonify(m_list)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        elif post.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        req_obj = User(**post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def show_by_user_id(user_id):
    """Retrieves a User object by id"""
    req_user = storage.get('User', user_id)
    if req_user is None:
        abort(404)
    if request.method == 'GET':
        """Retrieves a User by id"""
        return jsonify(req_user.to_dict())
    elif request.method == 'DELETE':
        """Deletes a User by id"""
        req_use = storage.get('User', user_id)
        storage.delete(req_use)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        """Updates a State object"""
        put = request.get_json()
        if put is None or type(put) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in put.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(req_user, key, value)
                storage.save()
        return jsonify(req_user.to_dict()), 200
