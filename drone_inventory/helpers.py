from functools import wraps
import secrets
from flask import request, jsonify, json
from drone_inventory.models import User
import decimal

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is Missing!'}), 401
        try:
            current_user_token = User.query.filter_by(token = token).first()
            # good to note here that filter_by is filtering by a kwarg, checking key-value pairs
            # as opposed to the filter we did yesterday in auth.routes
            print(current_user_token)
            if not current_user_token or current_user_token.token != token: 
                # current_user_token references the queried user above
                # current_user_token.token is referencing the user.token
                return jsonify({ 'message': 'Token is invalid!' })
        except:
            owner = User.query.filter_by(token=token).first()
            # owner and current_user_token are referencing the same user
            # basically, they picked a bad name for current_user_token
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return  jsonify({'message': 'Token is Invalid!'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # convert decimal instances (numerics) into strings so json can read it
            return str(obj)
        return super(JSONEncoder, self).default(obj)