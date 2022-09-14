import pupil_classes
import original_dataset_handler
import pupil_group_calculator
import asyncio


def try_distance():
    pupil1 = pupil_classes.Pupil("GU1 1SZ", False, False, 1)
    pupil2 = pupil_classes.Pupil("KT11 2AF", False, False, 1)

    print(pupil1.get_distance(pupil2))

async def try_pupil_time_seperation():
    pupils, pupils_willing_to_share = await original_dataset_handler.harvest_pupil_data_from_excel(get_pos_with_api=True, verbose=False)
    times_dict = pupil_group_calculator.seperate_pupils_by_times(pupils, 1, pupil_group_calculator.ArrivalOrDeparture.DEPARTURE)
    groups_of_groups = []
    for time, pupils in times_dict.items():
        groups = pupil_group_calculator.create_random_groups(pupils)
        groups_of_groups.append(groups)
    for groups in groups_of_groups:
        for i in range(10):
            print(f"iteration {i}", end=",   ")
            groups, improved = pupil_group_calculator.group_improvement_attempt_reorder(groups, False)
            groups, improved = pupil_group_calculator.group_improvement_attempt_remove_into_other_group(groups, 10000, False)
        print(f"Total length = {sum([g.route_length for g in groups])}, compared to {sum(sum(p.distance_to_school for p in g.people) for g in groups)}")
    

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(try_pupil_time_seperation())