class Song:
    def __init__(self, name: str, artist: str, album: str, length: int) -> None:
        self.name = name
        self.artist = artist
        self.album = album
        self.length = length

    def get_as_dict(self) -> dict:
        exprt_dict = {"name":self.name, "artist":self.artist, "album":self.album, "length":self.length}
        return exprt_dict