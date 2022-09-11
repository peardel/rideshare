import pandas as pd
import os
import tools

import pupil_classes

def harvest_pupil_data_from_excel(filename: str="OriginalDataset.xlsx", verbose: bool=True, get_pos_with_api: bool=True) -> tuple[list[pupil_classes.Pupil]]:
    if verbose: print(f"Harvesting pupil data from {filename}")
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data: pd.DataFrame = pd.read_excel(io=full_filename, header=0, names=None, index_col=None, usecols="A:N", true_values="YES", false_values="NO", nrows=101)

    pupils = []
    pupils_willing_to_share = []

    for item in data.iterrows():
        idx, information = item
        postcode, will_join_others, will_share_others, spare_seats, mon_arrival, mon_departure, tue_arrival, tue_departure, wed_arrival, wed_departure, thu_arrival, thu_departure, fri_arrival, fri_departure = information
        times = [[tools.time_string_to_int(x) for x in [arrival, departure]] for arrival, departure in [[mon_arrival, mon_departure], [tue_arrival, tue_departure], [wed_arrival, wed_departure], [thu_arrival, thu_departure], [fri_arrival, fri_departure]]]

        try:
            new_pupil = pupil_classes.Pupil(idx, tools.get_random_name(), postcode, will_join_others, will_share_others, spare_seats, times, get_pos_with_api=get_pos_with_api)
            if will_share_others == "YES": pupils_willing_to_share.append(pupil_classes)
            pupils.append(new_pupil)
        except IndexError:
            print(f"\tFailed for pupil #{idx}")
    
    print(f"Finished harvesting pupil data for {len(pupils)} pupils, {len(pupils_willing_to_share)} willing to share")
    return pupils, pupils_willing_to_share