import pandas
import openrouteservice
from pupil import Pupil

df = pandas.read_excel("OriginalDataset.xlsx")
print(df)

def coords():g

SCHOOL = Pupil("GU1 3BB", False, False, 0)
test_pupil = Pupil("KT13 8UW", False, False, 0)

client = openrouteservice.Client(key="5b3ce3597851110001cf6248b0c4037940f3452a988853816da080e9")
routes = client.directions()