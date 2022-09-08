import pandas as pd
import os

import tools
import pupil

def harvest_pupil_data_from_excel(filename: str="OriginalDataset.xlsx", verbose: bool=True) -> list[pupil.Pupil]:
    if verbose: print(f"Harvesting pupil data from {filename}")
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data: pd.DataFrame = pd.read_excel(io=full_filename, header=0, names=None, index_col=None, usecols="A:N", true_values="YES", false_values="NO", nrows=101)

    pupils = []
    for item in data.iterrows():
        idx, information = item
        postcode, will_join_others, will_share_others, spare_seats, mon_arrival, mon_departure, tue_arrival, tue_departure, wed_arrival, wed_departure, thu_arrival, thu_departure, fri_arrival, fri_departure = information

        # TODO: use the departure and arrival times

        new_pupil = pupil.Pupil(tools.get_random_name(), postcode, will_join_others, will_share_others, spare_seats)
        pupils.append(new_pupil)
    
    print(f"Finished harvesting pupil data for {len(pupils)} pupils")
    return pupils