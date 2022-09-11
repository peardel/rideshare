import requests
import json
import tools
import openrouteservice
import aiohttp

client = openrouteservice.Client(key="5b3ce3597851110001cf6248b0c4037940f3452a988853816da080e9")

SCHOOL_COORDINATES = (51.23738,-0.56944)

async def create_Pupil(id: int, name: str, postcode: str, will_join_others: bool, will_share_others: bool, spare_seats: int, times: list[tuple[int,int]], get_pos_with_api: bool = True):
    pupil = Pupil(id, name, postcode, will_join_others, will_share_others, spare_seats, times, get_pos_with_api)
    if get_pos_with_api: await pupil.position()

    return pupil

class Pupil:
    def __init__(self, id: int, name: str, postcode: str, will_join_others: bool, will_share_others: bool, spare_seats: int, times: list[tuple[int, int]], get_pos_with_api: bool = True):
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
        self.times = times
    
    async def position(self):
        url = f"https://findthatpostcode.uk/postcodes/{self.postcode.replace(' ', '%20')}.json"
        async with aiohttp.ClientSession() as session: # can only be instantiated inside an async function
            async with session.get(url) as r:
                if r.status == 404:
                    raise IndexError("Nonexistent Postcode")

                if r.status != 200:
                    raise Exception(f"HTTP error while getting coordinates of postcode {self.postcode}: status code {r.status}")
                
                res_json = await r.json()
                attributes = res_json["data"]["attributes"]
                self.latitude: float = attributes["lat"]
                self.longitude: float = attributes["long"]
                self.distance_to_school: float = tools.lat_lon_euclidean_dist(self.latitude, self.longitude, SCHOOL_COORDINATES[0], SCHOOL_COORDINATES[1])

    def get_distance_to_other_pupil(self, pupil: "Pupil") -> float:
        if abs(self.latitude) < 1 and abs(self.longitude) < 1:
            print(f"!!!!!{self.postcode}")
            raise Exception
        return tools.lat_lon_euclidean_dist(self.latitude, self.longitude, pupil.latitude, pupil.longitude)

    def __repr__(self) -> str:
        return f"{self.name}:\t {self.postcode},\t ({self.latitude}, {self.longitude}), WJ: {self.will_join_others}, WS: {self.will_share_others}, Spare Seats: {self.spare_seats}, "

coords = lambda A,B: ((A.longitude,A.latitude),(B.longitude,B.latitude))

def get_distance(pupil1: Pupil, pupil2: Pupil):
    routes = client.directions(coords(pupil1, pupil2))
    return routes["routes"][0]["summary"]["distance"]