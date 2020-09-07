from werkzeug.security import safe_str_cmp
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity

from models.user import UserModule
from config import jwt
from blacklist import BLACKLIST


# add claims to jwt token for authentication
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    current_user = UserModule.find_by_id(identity)
    if current_user["role"] == 'admin' or current_user["role"] == 'artist' or current_user["role"] == 'collector':
        return {
            'role': 'non_user'
        }
    return {'role': 'user'}

# create jwt access token
def access_token(_id, status):
    return create_access_token(_id, fresh=status)

#create jwt refresh token
def refresh_token(_id):
    return create_refresh_token(_id)

#create new access token from refresh token for authentication
@jwt_refresh_token_required
def recreate_access_token():
    current_user = get_jwt_identity()
    new_token = access_token(current_user, False)
    return new_token

#check jwt id in blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "msg": "Token has been revoked",
        "err": "token revoked"
    }), 401
