from flask import Flask, jsonify
from flask_restx import Api
from flask_cors import CORS
from app.config import config
from app.utils.database import init_db
from app.routes.user_routes import api as user_ns
import os

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    
    # Configure Swagger
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your bearer token in the format **Bearer &lt;token>**'
        }
    }
    
    api = Api(
        app,
        version='1.0',
        title='Flask Production API',
        description='A production-ready Flask REST API with Swagger documentation',
        authorizations=authorizations,
        security='Bearer Auth'
    )
    
    # Add namespaces
    api.add_namespace(user_ns, path='/api/users')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log error to stderr for Render logs
        import traceback
        import sys
        print(f"CRITICAL ERROR: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'type': e.__class__.__name__
        }), 500
    
    return app