import json
from json.decoder import JSONDecodeError, JSONDecoder
from json.encoder import JSONEncoder
from flask_restful import Resource
from classes.playlist import Playlist, deserialize_playlist
from classes.location import Location
from classes.song import Song
from classes.user import get_user, register_user
from classes.user import User

def update(user: User):
    f = open("users.json", "r+")
    data = {}
    try:
        data = json.load(f)
    except JSONDecodeError:
        pass
    data.update({user.uid:user.get_user_json()})
    open("users.json", "w+").write(JSONEncoder().encode(data))

class UserAPI(Resource):
    def get(self, uid):
        get_user(uid)

    def put(self, name):
        register_user(name)

class PlaylistAPI(Resource):
    def get(self, json):
        user_dict = JSONDecoder().decode(json)
        usr = get_user(user_dict['user_uid'])
        if user_dict['playlist_uid'] in usr.playlists:
            return usr.playlists['playlist_uid']

    def put(self, json):
        req_dict = JSONDecoder().decode(json)
        usr = get_user(req_dict['user_uid'])
        usr.add_playlist(Playlist(req_dict['name'], Location(req_dict['lat'], req_dict['long'], req_dict['pl_name'])))
        update(usr)
