from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    """Schema for user validation"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UserUpdateSchema(Schema):
    """Schema for user update validation"""
    username = fields.Str(validate=validate.Length(min=3, max=80))
    email = fields.Email()

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()