import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from rq import Queue
from worker import conn
from pusher import Pusher

app = Flask(__name__)
CORS(app)
app.secret_key = 'bkai@123'

queue = Queue(connection=conn)

pusher = Pusher(
    app_id="1068772",
    key="f9c2195a4cd9fefb3c71",
    secret="5b33122c131165580eba",
    cluster="ap1",
    ssl=True,
)

app.config['SECURITY_PASSWORD_SALT'] = 'this is super secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True



api = Api(app)
jwt = JWTManager(app)
