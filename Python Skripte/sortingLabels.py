from readCoordinates import read_coordinates
from writeCoordinates import write_coordinates


### Variables #####

info_data = 'inputs3/Info.csv'
coordinates_data = 'inputs3/Coordinates.csv'
destination = 'outputs3'
max_diff = {'x': 30, 'y': 30}   # maximum difference between 1 frame of the cmp-index of the coordinate
max_time_for_interpolating = 5.0  # in seconds

###################



# Reading the table

info, people = read_coordinates(info_data, coordinates_data, with_fillers=True)


not_found_temp = info['not_found'].strip('[]').split(', ')
not_found = ([int(not_found_temp[i]) for i in range(4)])
number_of_person = int(info['number_of_person'])
poss_wrong_det = int(info['poss_wrong_det'])
size_array = number_of_person + poss_wrong_det
FPS = float(info['FPS'])
cmp = {'x': 0, 'y': 1, 'width': 2, 'height': 3}


# Beginning of sorting
#######################

for person_count, person in enumerate(people):

    print("Person " + str(person_count))

    last_coordinates = [-1, -1, -1, -1]
    found = True
    gap_counter = 0

    if person_count >= number_of_person:
        break

    for index in range(len(person) - 1):

        # if the algorithm didn't find any coordinate for the next frame the last_coordinates becames the
        # last coordinate of the person and swaps the coordinate with the poss_wrong_det people who doesn't have any coordinate.
        # So the algorithm can search for the last_coordinate instead of not_found or another coordinate

        if (abs((person[index + 1][cmp['x']] - person[index][cmp['x']])) <= max_diff['x']) \
                and (abs((person[index + 1][cmp['y']] - person[index][cmp['y']])) <= max_diff['y']) \
                and found:
            continue

        elif found:  # check other person  in that frame

            found = False
            for i in range(size_array):

                if people[i] == person:
                    continue

                elif abs((people[i][index + 1][cmp['x']] - person[index][cmp['x']])) <= max_diff['x'] \
                        and abs((people[i][index + 1][cmp['y']] - person[index][cmp['y']])) <= max_diff['y']:

                    # found that coordinate in an other person in the same frame, so swap them
                    temp_coordinate = person[index + 1]
                    person[index + 1] = people[i][index + 1]
                    people[i][index + 1] = temp_coordinate
                    found = True
                    break

            if not found:  # set the last coordinate

                for i in range(poss_wrong_det):
                    # put the coordinate of the person of which the frame was not found to the extra people
                    # and check wether the extra person is filled with other coordinates or not
                    if people[number_of_person + i][index + 1] == not_found:
                        people[number_of_person + i][index + 1] = person[index + 1]
                        person[index + 1] = not_found
                        last_coordinates = person[index]
                        interpolate_start = {'coordinate': last_coordinates, 'index': index + 1}
                        break
                    elif i == poss_wrong_det - 1:
                        print("NOT ENOUGH EMPTY PEOPLE")


        # if the coordinate was not found
        else:

            gap_counter += 1

            # check the next coordinate with the last coordinate
            for i in range(size_array):

                if abs(people[i][index + 1][cmp['x']] - last_coordinates[cmp['x']]) <= max_diff['x']\
                        and abs(people[i][index + 1][cmp['y']] - last_coordinates[cmp['y']]) <= max_diff['y']:

                    if people[i] == person:
                        found = True
                        break

                    temp_coordinate = person[index + 1]
                    person[index + 1] = people[i][index + 1]
                    people[i][index + 1] = temp_coordinate
                    found = True
                    break

            if not found:  # if still not found
                for i in range(poss_wrong_det):
                    # put the coordinate of the person of which the frame was not found to the extra people
                    # and check wether the extra person is filled with other coordinates or not
                    if people[number_of_person + i][index + 1] == not_found:
                        people[number_of_person + i][index + 1] = person[index + 1]
                        person[index + 1] = not_found
                        break

            else:  # Interpolating

                if gap_counter/FPS <= max_time_for_interpolating:
                    interpolate_end = {'coordinate': person[index + 1], 'index': index + 1}

                    x_diff = interpolate_end['coordinate'][cmp['x']] - interpolate_start['coordinate'][cmp['x']]
                    y_diff = interpolate_end['coordinate'][cmp['y']] - interpolate_start['coordinate'][cmp['y']]
                    width_diff = interpolate_end['coordinate'][cmp['width']] - interpolate_start['coordinate'][cmp['width']]
                    height_diff = interpolate_end['coordinate'][cmp['height']] - interpolate_start['coordinate'][cmp['height']]

                    for k, indx in enumerate(range(interpolate_start['index'], interpolate_end['index'])):

                        x = interpolate_start['coordinate'][cmp['x']] + int(x_diff * ((k+1)/gap_counter))
                        y = interpolate_start['coordinate'][cmp['y']] + int(y_diff * ((k+1)/gap_counter))
                        width = interpolate_start['coordinate'][cmp['width']] + int(width_diff * ((k+1)/gap_counter))
                        height = interpolate_start['coordinate'][cmp['height']] + int(height_diff * ((k+1)/gap_counter))

                        if x < 0 or y < 0 or width < 0 or height < 0:  # when there are some problems
                            print("THERE ARE SOME PROBLEMS IN INTERPOLATING!! The frame number is " + str(indx))
                            x = y = width = height = 0

                        person[indx] = [x, y, width, height]

                    gap_counter = 0

                else:
                    gap_counter = 0




# End of Sorting
#################

destination = destination + '/Sortierte Koordinaten.csv'

write_coordinates(people, size_array, destination)

