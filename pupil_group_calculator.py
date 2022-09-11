from argparse import ArgumentError
import pupil_classes
import tools

import random
from enum import IntEnum
import math

class ArrivalOrDeparture(IntEnum):
    ARRIVAL = 0
    DEPARTURE = 1

class Group:
    def __init__(self, driver: pupil_classes.Pupil) -> None:
        self.people: list[pupil_classes.Pupil] = [driver]
        self.route_length = driver.distance_to_school

    @property
    def driver(self) -> pupil_classes.Pupil:
        return self.people[0]

    @property
    def last_person(self) -> pupil_classes.Pupil:
        return self.people[-1]

    def can_take_another_pupil(self) -> bool:
        return self.driver.spare_seats+1 > len(self.people)

    def add_pupil(self, new_pupil: pupil_classes.Pupil):
        if new_pupil in self.people:
            raise ArgumentError("Cannot add pupil to group as already in group")
        if not self.can_take_another_pupil():
            raise ArgumentError(f"Driver #{self.driver.id} cannot fit another pupil in car, already has [{' ,'.join(f'#{p.id}' for p in self.people[1:])}] and only has {self.driver.spare_seats} spare seats")
        self.route_length += self.query_route_extension_if_add_new_pupil(new_pupil)
        self.people.append(new_pupil)

    def query_route_extension_if_add_new_pupil(self, new_pupil: pupil_classes.Pupil) -> float:
        return new_pupil.distance_to_school - self.last_person.distance_to_school + self.last_person.get_distance_to_other_pupil(new_pupil)

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
    # nominate random group drivers till we run out people
    groups: "list[Group]" = []
    pupils_willing_to_share_and_join = [pupil for pupil in pupils if pupil.will_share_others]
    pupils_willing_to_share_only = [pupil for pupil in pupils if pupil.will_share_others and not pupil.will_join_others]
    pupils_freeloading = [pupil for pupil in pupils if not pupil.will_share_others]
    # all these lists above are mutually exclusive

    random.shuffle(pupils_willing_to_share_and_join)
    random.shuffle(pupils_freeloading)

    # first give people willing to share only their own groups
    for pupil in pupils_willing_to_share_only:
        groups.append(Group(driver=pupil))

    # prioritise "using up" the people who wont share   
    for pupil in pupils_freeloading:
        # find the group where it would add the least number of miles
        # TODO: make a new group if no groups exist which can take a new passenger (very rare occurence)
        best_group = min([group for group in groups if group.can_take_another_pupil()], key=lambda group: group.query_route_extension_if_add_new_pupil(pupil))
        best_group.add_pupil(pupil)
    
    for pupil in pupils_willing_to_share_and_join:
        # see which group is best to add them to
        best_dist = math.inf
        for group in [group for group in groups if group.can_take_another_pupil()]:
            dist = group.query_route_extension_if_add_new_pupil()