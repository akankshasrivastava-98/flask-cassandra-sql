from flask import Blueprint
from flask_restplus import Api
from werkzeug.utils import cached_property
from collections.abc import MutableMapping

from .apiHandler import api as new_api


blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='demo sql',
          version='1.0',
          description='demo sql',
          contact="Akanksha Srivastav",
          )

api.add_namespace(new_api)

