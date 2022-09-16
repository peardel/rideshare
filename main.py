import original_dataset_handler
import asyncio
import pupil_group_calculator
import visualizer

async def main():
    print("Obtaining pupil data...")
    all_pupils = await original_dataset_handler.harvest_pupil_data_from_excel(get_pos_with_api=True, verbose=False)
    print("Finished harvesting data.")

    results = []

    for day, day_string in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")):
        for arrival_or_departure in (pupil_group_calculator.ArrivalOrDeparture.ARRIVAL, pupil_group_calculator.ArrivalOrDeparture.DEPARTURE):
            times_dict = pupil_group_calculator.seperate_pupils_by_times(all_pupils, day, arrival_or_departure, verbose=False)
            groups_for_each_time = []
            for time, pupils in times_dict.items():
                groups = pupil_group_calculator.create_random_groups(pupils, verbosity=0)
                groups_for_each_time.append(groups)
            
            # do the calculations
            for i,groups in enumerate(groups_for_each_time):
                for j in range(5):
                    groups, improved = pupil_group_calculator.group_improvement_attempt_reorder(groups, False)
                    groups, improved = pupil_group_calculator.group_improvement_attempt_remove_into_other_group(groups, 1000, False)
                    
                groups_for_each_time[i] = groups
            total_original_length = sum(pupil_group_calculator.get_total_original_length_of_groups(groups) for groups in groups_for_each_time)
            total_new_length = sum(pupil_group_calculator.get_total_length_of_groups(groups) for groups in groups_for_each_time)
            print(f"For {day_string} {['AM', 'PM'][arrival_or_departure]},\tOriginal Route Lengths: {total_original_length:.3f}km, New: {total_new_length:.3f}km. Saved {total_original_length-total_new_length:.3f}km and {0.275*(total_original_length-total_new_length):.2f}kg of CO2")
            
            result = {
                "day": day_string,
                "departure": arrival_or_departure,
                "groups": groups_for_each_time,
                "original_length": total_original_length,
                "total_new_length": total_new_length
            }

            results.append(result)
    
    print("Opening PyGame window to visualise results... (hover over each point to view details, use buttons or arrow keys to scroll through session times)")

    await visualizer.visualize(results)

asyncio.run(main())