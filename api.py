import json
from json.decoder import JSONDecodeError, JSONDecoder
from json.encoder import JSONEncoder
from flask_restful import Resource
from classes.playlist import Playlist, deserialize_playlist
from classes.location import Location
from classes.song import Song
from classes.user import get_user, register_user, User

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
    # get playlist
    def get(self, json):
        user_dict = JSONDecoder().decode(json)
        usr = get_user(user_dict['user_uid'])
        if user_dict['playlist_uid'] in usr.playlists:
            plist = usr.playlists['playlist_uid']
            if plist.available():
                return plist

    # add playlist
    def put(self, json):
        req_dict = JSONDecoder().decode(json)
        usr = get_user(req_dict['user_uid'])
        usr.add_playlist(Playlist(req_dict['name'], Location(req_dict['lat'], req_dict['long'], req_dict['pl_name'])))
        update(usr)

class SongAPI(Resource):
    def get(self, json): # must contain user uid, playlist uid, and song name
        user_dict = JSONDecoder().decode(json)
        usr = get_user(user_dict['user_uid'])
        if user_dict['playlist_uid'] in usr.playlists:
            playlist = deserialize_playlist(usr.playlists['playlist_uid'])
            return playlist.get_song(user_dict['song_name'])

    def put(self, json): # must contain user uid, playlist uid, and song info
        req_dict = JSONDecoder().decode(json)
        usr = get_user(req_dict['user_uid'])
        usr.playlists['playlist_uid'].add_song(Song(req_dict['song_name'], req_dict['song_artist'], req_dict['song_album'], req_dict['song_length']))
        update(usr)