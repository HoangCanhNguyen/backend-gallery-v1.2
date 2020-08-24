from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from flask import jsonify

from config import app

ma = Marshmallow()


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
  return jsonify(err.messages), 400