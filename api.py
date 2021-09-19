from json.decoder import JSONDecoder
from flask_restful import Resource
from classes.playlist import Playlist, deserialize_playlist
from classes.location import Location
from classes.song import Song
from classes.user import get_user, register_user

class UserAPI(Resource):
    def get(self, uid):
        get_user(uid)

    def put(self, name):
        register_user(name)

class PlaylistAPI(Resource):
    def get(self, json):
        user_dict = JSONDecoder().decode(json)
        usr = get_user(user_dict['user'])
        for playlist in user_dict['playlists']:
            deserialize_playlist(playlist)
        