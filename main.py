import pandas
import openrouteservice
import original_dataset_handler
import asyncio
from pupil_classes import create_Pupil, Pupil

df = pandas.read_excel("OriginalDataset.xlsx")

coords = lambda A,B: ((A.longitude,A.latitude),(B.longitude,B.latitude))

MAX_DISTANCE_TRAVELLABLE = 0.1
client = openrouteservice.Client(key="5b3ce3597851110001cf6248b0c4037940f3452a988853816da080e9") # distance calcs should only be used to go to school, not to compare with other students

def get_distance_to_school(pupil: Pupil, SCHOOL: Pupil):
    routes = client.directions(coords(pupil, SCHOOL))
    return routes["routes"][0]["summary"]["distance"]

async def main():
    SCHOOL = await create_Pupil(-1, "SCHOOL", "GU1 3BB", False, False, 0, (0,0))
    pupils, pupils_willing_to_drive = await original_dataset_handler.harvest_pupil_data_from_excel()
    for pupil in pupils:
        print(pupil)

asyncio.run(main())