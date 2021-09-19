class Location:
    def __init__(self, latitude, longitude, custom_name) -> None:
        self.lat = latitude
        self.long = longitude
        self.name = custom_name

    def __eq__(self, other) -> bool:
        return self.lat == other.lat and self.long == other.long

    def __repr__(self):
        return "(" + str(self.lat) + "," + str(self.long) + "), " + self.name

    def as_dict(self):
        return {"lat":self.lat, "long":self.long, "name":self.name}