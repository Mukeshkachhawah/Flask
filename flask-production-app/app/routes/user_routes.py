from flask_restx import Namespace, Resource, fields
from app.services.user_service import UserService

# Create namespace for Swagger
api = Namespace('users', description='User operations')

# Swagger models
user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'created_at': fields.DateTime(readOnly=True, description='Creation date'),
    'updated_at': fields.DateTime(readOnly=True, description='Update date')
})

user_response_model = api.model('UserResponse', {
    'id': fields.Integer(readOnly=True, description='User ID'),
    'username': fields.String(description='Username'),
    'email': fields.String(description='Email address'),
    'created_at': fields.DateTime(readOnly=True, description='Creation date'),
    'updated_at': fields.DateTime(readOnly=True, description='Update date')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        return UserService.get_all_users()
    
    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201)
    @api.response(409, 'User already exists')
    def post(self):
        """Create a new user"""
        return UserService.create_user(api.payload)

@api.route('/<int:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user by ID"""
        result = UserService.get_user_by_id(user_id)
        if result is None:
            api.abort(404, 'User not found')
        return result
    
    @api.doc('update_user')
    @api.expect(api.model('UserUpdate', {
        'username': fields.String(description='Username'),
        'email': fields.String(description='Email address')
    }))
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update user"""
        return UserService.update_user(user_id, api.payload)
    
    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete user"""
        return UserService.delete_user(user_id)