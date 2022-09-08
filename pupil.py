import requests
import json
import tools

class Pupil:
    def __init__(self, name: str, postcode: str, will_join_others: bool, will_share_others: bool, spare_seats: int):
        '''
        needs lat and long using apis and stuff
        '''
        self.name: str = name
        self.postcode: str = postcode
        self.will_join_others: bool = will_join_others
        self.will_share_others: bool = will_share_others
        self.spare_seats: int = spare_seats

        self.failed = False
        success = self.get_coordinates()
        if success is False:
            raise IndexError("Nonexistent postcode")
        url = f"https://findthatpostcode.uk/postcodes/{self.postcode.replace(' ', '%20')}.json"
        r = requests.get(url)

        if r.status_code == 404:
            return False

        if r.status_code != 200:
            raise Exception(f"HTTP error while getting coordinates of postcode {self.postcode}: status code {r.status_code}")
        
        attributes = r.json()["data"]["attributes"]
        self.latitude: float = attributes["lat"]
        self.longitude: float = attributes["long"]

        return True

    def get_distance(self, pupil: "Pupil") -> float:
        return tools.lat_lon_euclidean_dist(self.latitude, self.longitude, pupil.latitude, pupil.longitude)