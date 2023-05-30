#!/usr/bin/python3
"""new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from datetime import datetime
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
import uuid

if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def list_ame_by_place_id(place_id):
        """Retrieves the list of all Amenity objects of a Place"""
        req_amen = storage.get('Place', place_id)
        if req_amen is None:
            abort(404)
        return jsonify([val.to_dict() for val in req_amen.amenities])


    @app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                     methods=['POST', 'DELETE'], strict_slashes=False)
    def del_create_amenity(place_id, amenity_id):
        place = storage.get('Place', place_id)
        if place is None:
            abort(404)
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404)
        elif request.method == 'DELETE':
            """Deletes a Amenity object to a Place"""
            all_places = storage.all("Place").values()
            place_obj = [obj.to_dict() for obj in all_places
                         if obj.id == place_id]
            if place_obj == []:
                abort(404)

            all_amenities = storage.all("Amenity").values()
            amenity_obj = [obj.to_dict() for obj in all_amenities
                           if obj.id == amenity_id]
            if amenity_obj == []:
                abort(404)
            amenity_obj.remove(amenity_obj[0])

            for obj in all_places:
                if obj.id == place_id:
                    if obj.amenities == []:
                        abort(404)
                    for amenity in obj.amenities:
                        if amenity.id == amenity_id:
                            storage.delete(amenity)
                            storage.save()
            return jsonify({}), 200
        elif request.method == 'POST':
            """Link a Amenity object to a Place"""
            all_places = storage.all("Place").values()
            place_obj = [obj.to_dict() for obj in all_places
                         if obj.id == place_id]
            if place_obj == []:
                abort(404)

            all_amenities = storage.all("Amenity").values()
            amenity_obj = [obj.to_dict() for obj in all_amenities
                           if obj.id == amenity_id]
            if amenity_obj == []:
                abort(404)

            amenities = []
            for place in all_places:
                if place.id == place_id:
                    for amenity in all_amenities:
                        if amenity.id == amenity_id:
                            place.amenities.append(amenity)
                            storage.save()
                            amenities.append(amenity.to_dict())
                            return jsonify(amenities[0]), 200
            return jsonify(amenities[0]), 201
