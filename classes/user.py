import base64
from json.encoder import JSONEncoder
from json.decoder import JSONDecodeError, JSONDecoder
import json
from os import write
import uuid

from classes.playlist import deserialize_playlist

class User:
    def __init__(self, username, uid=None, playlists=[]) -> None:
        self.playlists = playlists
        if not uid:
            uid = str(uuid.uuid4())
        self.uid = uid
        self.username = username

    def add_playlist(self, p):
        self.playlists += [p]
        self.playlists = sorted(self.playlists)

    def remove_playlist(self, p):
        self.playlists.remove(p)

    # api methods
    def get_user_json(self) -> str:
        export_dict = {}
        export_dict.update({"name":self.username})
        export_dict.update({"uid":str(self.uid)})
        export_dict.update({"playlists":[playlist.get_as_dict() for playlist in self.playlists]})
        return JSONEncoder().encode(export_dict)
    
def deserialize_user(json_str:str) -> User:
    data = JSONDecoder().decode(json_str)
    name = data['name']
    uid = data['uid']
    playlists = [deserialize_playlist(playlist) for playlist in data['playlists']]
    return User(name, uid, playlists)


def get_user(uid: str) -> bytes:
    f = open("users.json", "r")
    data = json.load(f)
    if uid in data:
        return base64.b64encode(deserialize_user(data[uid]))
    else:
        return None


def register_user(json_str: str) -> int:
    f = open("users.json", "r+")
    new_data = JSONDecoder().decode(json_str)
    data = {}
    try:
        data = json.load(f)
        print(data)
        for uid in data:
            if json.loads(data[uid])['name'] == new_data['name']:
                return 1
    except JSONDecodeError:
        pass
    newUser = User(new_data['name'])
    data.update({newUser.uid:newUser.get_user_json()})
    print(data)
    open("users.json", "w+").write(json.dumps(JSONEncoder().encode(data), indent=4))
    return 0
    



