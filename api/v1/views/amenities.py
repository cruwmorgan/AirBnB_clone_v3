#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities_list():
    """Retrieves the list of all Amenity objects"""
    if request.method == 'GET':
        m_list = []
        for obj in storage.all(Amenity).values():
            m_list.append(obj.to_dict())
        return jsonify(m_list)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        req_obj = Amenity(**post)
        req_obj.save()
        return jsonify(req_obj.to_dict()), 201


@app_views.route('amenities/<string:amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def show_by_amenity_id(amenity_id):
    """Retrieves a Amenity object by id"""
    req_ame = storage.get('Amenity', amenity_id)
    if req_ame is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(req_ame.to_dict())
    elif request.method == 'DELETE':
        req_ame = storage.get('Amenity', amenity_id)
        storage.delete(req_ame)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        """Updates a State object"""
        put = request.get_json()
        if put is None or type(put) != dict:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in put.items():
            setattr(req_ame, key, value)
            storage.save()
        return jsonify(req_ame.to_dict()), 200
