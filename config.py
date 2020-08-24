from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.secret_key = 'bkai@123'

app.config['SECURITY_PASSWORD_SALT'] = 'this is super secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

jwt = JWTManager(app)
