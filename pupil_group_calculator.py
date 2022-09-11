from argparse import ArgumentError
import pupil_classes
import tools

import random
from enum import IntEnum
import math
import itertools

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
        self.route_length += self.query_route_extension_if_append_new_pupil(new_pupil)
        self.people.append(new_pupil)

    def query_route_extension_if_append_new_pupil(self, new_pupil: pupil_classes.Pupil) -> float:
        return new_pupil.distance_to_school - self.last_person.distance_to_school + self.last_person.get_distance_to_other_pupil(new_pupil)

    def query_route_extension_if_insert_new_pupil(self, new_pupil: pupil_classes.Pupil, index: int) -> float:
        if index > len(self.people):
            raise ArgumentError("Cannot insert beyond end of people list")
        if index == len(self.people):
            return self.query_route_extension_if_append_new_pupil(new_pupil)
        if index == 0:
            return new_pupil.get_distance_to_other_pupil(self.driver)
        return new_pupil.get_distance_to_other_pupil(self.people[index]) + self.people[index-1].get_distance_to_other_pupil(new_pupil) - self.people[index-1].get_distance_to_other_pupil(self.people[index])

def seperate_pupils_by_times(pupils: list[pupil_classes.Pupil], day: int, arrival_or_departure: ArrivalOrDeparture, verbose: bool=True) -> dict[int, list[pupil_classes.Pupil]]:
    pupils_times: list[int] = [pupil.times[day][arrival_or_departure] for pupil in pupils]
    pupil_sections: dict[int, list[pupil_classes.Pupil]] = {pupil_time: [] for pupil_time in pupils_times}
    for i, pupil in enumerate(pupils):
        pupil_sections[pupils_times[i]].append(pupil)
    print(f"Found possible times of [{', '.join(tools.int_to_time_string(t_s) for t_s in pupil_sections.keys())}]")
    for time, pupils_in_section in pupil_sections.items():
        print(f"\t{tools.int_to_time_string(time)}: [{', '.join(f'#{str(pupil.id).zfill(2)}' for pupil in pupils_in_section)}]")
    return pupil_sections

def create_random_groups(pupils: list[pupil_classes.Pupil], verbosity:int=2) -> list[list[pupil_classes.Pupil]]:
    if verbosity >= 1: print(f"Creating random groups with pupils {', '.join(f'#{str(p.id)}' for p in pupils)}")
    # nominate random group drivers till we run out people
    groups: "list[Group]" = []
    pupils_willing_to_share_and_join = [pupil for pupil in pupils if pupil.will_share_others and pupil.will_join_others]
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
        best_group = None
        for group in [group for group in groups if group.can_take_another_pupil()]:
            dist = group.query_route_extension_if_add_new_pupil(pupil)
            if dist < best_dist:
                dist = best_dist
                best_group = group
        if best_group is None or best_dist > pupil.distance_to_school:
            # make a new group with this person
            groups.append(Group(pupil))
        else:
            best_group.add_pupil(pupil)

    for group in groups:
        if verbosity >= 2: print(f"\tGroup with driver #{group.driver.id}: [{', '.join(f'#{str(p.id)}' for p in group.people)}] (max {group.driver.spare_seats}) ({'wants' if group.driver.will_share_others else 'doesnt want'} to share) ({'wants' if group.driver.will_join_others else 'doesnt want'} to join)")

    return groups

def group_improvement_attempt_reorder(groups: list[Group], verbose=False) -> tuple[list[Group], bool]:
    if verbose: print(f"Attempting to reorder groups [{',  '.join(f'#{g.driver.id}' for g in groups)}]")
    made_an_improvement = False
    for group in groups:
        # try to shuffle the group and see what happens
        if len(group.people) == 1: continue
        original_route_length = group.route_length
        best_new_route_length = original_route_length
        new_perm = None
        for perm in itertools.permutations(group.people):
            if perm == group.people: continue # this is the original
            if not perm[0].will_share_others: continue # the driver doesn't want to share
            if perm[0].spare_seats+1 < len(group.people): continue # the driver doesn't have enough seats
            everyone_riding_wants_to_join = True
            for person in perm[1:]:
                if not person.will_join_others:
                    everyone_riding_wants_to_join = False
                    break
            if not everyone_riding_wants_to_join: continue # there are passengers who dont want to join
            # ok, then calculate the new length of the route
            new_route_length = 0
            for i in range(len(group.people) - 1):
                new_route_length += perm[i].get_distance_to_other_pupil(perm[i+1])
            new_route_length += perm[-1].distance_to_school
            if new_route_length < best_new_route_length:
                new_perm = perm
                best_new_route_length = new_route_length

        if new_perm is not None:
            # we have found a better ordering of everyone
            made_an_improvement = True
            if verbose: print(f"Group went from [{', '.join(f'#{p.id}' for p in group.people)}] with length {group.route_length}, to: ", end="")
            group.people = new_perm
            group.route_length = best_new_route_length
            if verbose: print(f"[{', '.join(f'#{p.id}' for p in group.people)}] with length {group.route_length}")

    return groups, made_an_improvement

def group_improvement_attempt_remove_into_other_group(groups: list[Group], iterations:int = 100, verbose=False) -> tuple[list[Group], bool]:
    made_improvement = False
    for iteration in iterations:
        # pick a random group
        groups_with_passengers = [g for g in groups if len(g) > 1]
        if len(groups_with_passengers) == 0:
            return groups, made_improvement
        main_group: Group = random.choice(groups_with_passengers)
        original_route_length = main_group.route_length
        really_best_other_group = None
        really_best_other_group_position = None
        really_best_new_route_length = original_route_length
        for i, person in enumerate(main_group.people):
            if i == 0: continue # dont remove driver
            new_route_length = original_route_length
            if i == len(main_group.people)-1: # this person is at the end
                new_route_length += main_group.people[i-1].distance_to_school
                new_route_length -= person.distance_to_school
                new_route_length -= main_group.people[i-1].get_distance_to_other_pupil(person)
            else:
                new_route_length += main_group.people[i-1].get_distance_to_other_pupil(main_group.people[i+1])
                new_route_length -= main_group.people[i-1].get_distance_to_other_pupil(person)
                new_route_length -= person.get_distance_to_other_pupil(main_group.people[i+1])
            # that is the new route length for the original group, but we must also factor in this person going into another group instead
            # just go thru all the groups and all the positions and see if theyre good
            best_other_group = None
            best_other_group_position = None
            best_route_extension = math.inf
            for other_group in groups:
                if other_group == main_group: continue
                if not other_group.can_take_another_pupil(): continue
                for other_group_index in range(len(other_group.people)):
                    if other_group_index == 0 and (not person.will_share_others or not other_group.driver.will_join_others): continue
                    route_extension = other_group.query_route_extension_if_insert_new_pupil(person, other_group_index)
                    if route_extension < best_route_extension:
                        best_other_group = other_group
                        best_other_group_position = other_group_index
                        best_route_extension = route_extension
            
            if new_route_length + best_route_extension < really_best_new_route_length: # found new better configuration!
                really_best_other_group = best_other_group
                really_best_other_group_position = best_other_group_position
                really_best_new_route_length = new_route_length + best_route_extension

                # WIP