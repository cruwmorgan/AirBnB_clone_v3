#!/usr/bin/python3
"""return JSON status ok
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def app_status():
    """check the status of api"""
    return jsonify({'status': 'OK'})
