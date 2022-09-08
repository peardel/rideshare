import pandas
import random
import openrouteservice
import original_dataset_handler
from pupil import Pupil

pupils = original_dataset_handler.harvest_pupil_data_from_excel()
test_pupil = random.choice([p for p in pupils if not p.failed])

client = openrouteservice.Client(key="5b3ce3597851110001cf6248b0c4037940f3452a988853816da080e9")
routes = client.directions()