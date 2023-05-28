#!/usr/bin/python3
"""return JSON status ok
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def app_status():
    """check the status of api"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_number():
    """an endpoint that retrieves the number of each objects by type:
    """
    objects = {
        "amenities": 'Amenity',
        "cities": 'City',
        "places": 'Place',
        "reviews": 'Review',
        "states": 'State',
        "users": 'User'
    }
    temp_dict = {}
    for key, value in objects.items():
        temp_dict[key] = storage.count(value)
    return jsonify(temp_dict)


if __name__ == "__main__":
    pass
