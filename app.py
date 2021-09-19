import api

from flask import Flask
from flask_restful import Api
app = Flask("Localized Spotify")
api = Api(app)

api.add_resource(api.ProjectAPI, '/playlist_ctrl/<str:json>') # must contain uid and playlist uid
api.add_resource(api.UserAPI, '/users/<str:json>')