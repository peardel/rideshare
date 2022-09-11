import pupil_classes
import tools

from enum import IntEnum

# Group datatype = list of pupils, order = order in which they drive

class ArrivalOrDeparture(IntEnum):
    ARRIVAL = 0
    DEPARTURE = 1

def seperate_pupils_by_times(pupils: list[pupil_classes.Pupil], day: int, arrival_or_departure: ArrivalOrDeparture, verbose: bool=True) -> dict[int, list[pupil_classes.Pupil]]:
    pupils_times: list[int] = [pupil.times[day][arrival_or_departure] for pupil in pupils]
    pupil_sections: dict[int, list[pupil_classes.Pupil]] = {pupil_time: [] for pupil_time in pupils_times}
    for i, pupil in enumerate(pupils):
        pupil_sections[pupils_times[i]].append(pupil)
    print(f"Found possible times of [{', '.join(tools.int_to_time_string(t_s) for t_s in pupil_sections.keys())}]")
    for time, pupils_in_section in pupil_sections.items():
        print(f"\t{tools.int_to_time_string(time)}: [{', '.join(f'#{str(pupil.id).zfill(2)}' for pupil in pupils_in_section)}]")
    return pupil_sections

def create_random_groups(pupils: list[pupil_classes.Pupil]) -> list[list[pupil_classes.Pupil]]:
    pass