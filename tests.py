import pupil_classes
import original_dataset_handler
import pupil_group_calculator
import asyncio


def try_distance():
    pupil1 = pupil_classes.Pupil("GU1 1SZ", False, False, 1)
    pupil2 = pupil_classes.Pupil("KT11 2AF", False, False, 1)

    print(pupil1.get_distance(pupil2))

async def try_pupil_time_seperation():
    pupils, pupils_willing_to_share = await original_dataset_handler.harvest_pupil_data_from_excel(get_pos_with_api=True)
    times_dict = pupil_group_calculator.seperate_pupils_by_times(pupils, 0, pupil_group_calculator.ArrivalOrDeparture.DEPARTURE)
    groups_of_groups = []
    for time, pupils in times_dict.items():
        groups = pupil_group_calculator.create_random_groups(pupils)
        groups_of_groups.append(groups)
    for groups in groups_of_groups:
        groups, improved = pupil_group_calculator.group_improvement_attempt_reorder(groups, True)
        groups, improved = pupil_group_calculator.group_improvement_attempt_remove_into_other_group(groups, True)
    

asyncio.run(try_pupil_time_seperation())