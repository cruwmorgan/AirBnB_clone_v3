#!/usr/bin/python3
"""return the status of your API
"""
from os import getenv
from flask import Flask, jsonify, Blueprint, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """method to handle @app.teardown_appcontext that calls storage.close
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles error 404 by responding with JSON
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
            threaded=True, debug=True)
