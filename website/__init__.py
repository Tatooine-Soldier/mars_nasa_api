from enum import unique
from flask import Flask, jsonify, request, render_template



def create_app(): 
    app = Flask(__name__)

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')

    return app