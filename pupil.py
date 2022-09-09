import requests
import json
import tools
import openrouteservice

client = openrouteservice.Client(key="5b3ce3597851110001cf6248b0c4037940f3452a988853816da080e9")

class Pupil:
    def __init__(self, id: int, name: str, postcode: str, will_join_others: bool, will_share_others: bool, spare_seats: int):
        '''
        needs lat and long using apis and stuff
        '''
        str_to_bool = lambda b: b if isinstance(b, bool) else {"YES": True, "NO": False}[b]

        self.id: int = id
        self.name: str = name
        self.postcode: str = postcode
        self.will_join_others: bool = str_to_bool(will_join_others)
        self.will_share_others: bool = str_to_bool(will_share_others)
        self.spare_seats: int = spare_seats
   
        url = f"https://findthatpostcode.uk/postcodes/{self.postcode.replace(' ', '%20')}.json"
        r = requests.get(url)

        if r.status_code == 404:
            raise IndexError("Nonexistent Postcode")

        if r.status_code != 200:
            raise Exception(f"HTTP error while getting coordinates of postcode {self.postcode}: status code {r.status_code}")
        
        attributes = r.json()["data"]["attributes"]
        self.latitude: float = attributes["lat"]
        self.longitude: float = attributes["long"]

    def get_distance(self, pupil: "Pupil") -> float:
        return tools.lat_lon_euclidean_dist(self.latitude, self.longitude, pupil.latitude, pupil.longitude)

    def __repr__(self) -> str:
        return f"{self.name}:\t {self.postcode},\t ({self.latitude}, {self.longitude}), WJ: {self.will_join_others}, WS: {self.will_share_others}, Spare Seats: {self.spare_seats}, "

coords = lambda A,B: ((A.longitude,A.latitude),(B.longitude,B.latitude))

def get_distance(pupil1: Pupil, pupil2: Pupil):
    routes = client.directions(coords(pupil1, pupil2))
    return routes["routes"][0]["summary"]["distance"]

class Car:
    def __init__(self, driver):
        self.pupils = [driver] # order matters
    
    def get_distance(self):
        distance = 0

        for i,pupil in enumerate(self.pupils):
            if i == len(self.pupils)-1:
                target = Pupil("SCHOOL", "GU1 3BB", False, False, 0)
            else:
                target = self.pupils[i+1]
            
            distance += get_distance(pupil,target)

        return distance