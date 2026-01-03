from app.models.user import User
from app.utils.database import db
from app.schemas.user_schemas import user_schema, user_update_schema
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    """Service for user operations"""
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        users = User.query.all()
        return user_schema.dump(users, many=True)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        if not user:
            return None
        return user_schema.dump(user)
    
    @staticmethod
    def create_user(data):
        """Create new user"""
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 409
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 409
        
        # Hash password
        hashed_password = generate_password_hash(data['password'])
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    
    @staticmethod
    def update_user(user_id, data):
        """Update user"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate update data
        errors = user_update_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # Update fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return user_schema.dump(user), 200
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user"""
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None