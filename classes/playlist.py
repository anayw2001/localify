from classes.song import Song
from classes.location import Location
from functools import total_ordering
import time
import uuid
from json.encoder import JSONEncoder

@total_ordering
class Playlist:

    def __init__(self, name: str, location: Location) -> None:
        self.songs = []
        self.name = name
        self.uid = str(uuid.uuid4())
        self.location = location
        self.date_created = time.time()

    # Comparison methods
    def __lt__(self, other) -> bool:
        return (self.name < other.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    # Utility methods
    def available(self, location: Location):
        return self.location == location
    
    def add_song(self, song: Song) -> None:
        self.songs.append(song)

    def remove_song(self, song: Song) -> None:
        self.songs.remove(song)

    # API internal
    def api_export(self) -> str:
        return JSONEncoder().encode(self.get_as_dict())

    def get_as_dict(self) -> dict:
        exprt_dict = {}
        exprt_dict = {"name": self.name, "uid":self.uid, "location":self.location.as_dict(), "date_created":str(self.date_created)}
        exprt_dict.update({"songs":[song.get_as_dict() for song in self.songs]})
        return exprt_dict

def deserialize_playlist(import_dict: dict) -> Playlist:
    loc = Location(import_dict['location']['lat'], import_dict['location']['long'], import_dict['location']['name'])
    plist = Playlist(import_dict['name'], loc)
    plist.date_created = float(import_dict['date_created'])
    plist.uid = import_dict['uid']
    for song in import_dict['songs']:
        song = Song(song['name'], song['artist'], song['album'], song['length'])
        plist.add_song(song)
    return plist