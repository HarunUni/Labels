"""Cleaner try of sorting the coordinates."""

from readCoordinates import read_coordinates
from writeCoordinates import write_coordinates


### Variables #####

info_data = 'inputs1/Info.csv'
coordinates_data = 'inputs1/Sortierte Koordinaten 2.csv'
destination = 'outputs1'
max_diff = {'x': 100, 'y': 100, 'width': 20, 'height': 20}   # maximum difference between 1 frame of the cmp-index of the coordinate
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

    if person_count >= number_of_person:
        break

    print("Person " + str(person_count))

    last_coordinates = [-1, -1, -1, -1]
    found = True
    gap_counter = 0

    for index in range(len(person) - 1):

        # if the algorithm didn't find any coordinate for the next frame the last_coordinates becames the
        # last coordinate of the person and swaps the coordinate with the poss_wrong_det people who doesn't have any coordinate.
        # So the algorithm can search for the last_coordinate instead of not_found or another coordinate

        if (abs((person[index + 1][cmp['x']] - person[index][cmp['x']])) <= max_diff['x']) \
                and (abs((person[index + 1][cmp['y']] - person[index][cmp['y']])) <= max_diff['y']) \
                and (abs((person[index + 1][cmp['width']] - person[index][cmp['width']])) <= max_diff['width']) \
                and (abs((person[index + 1][cmp['height']] - person[index][cmp['height']])) <= max_diff['height']) \
                and found:
            continue

        else:  # check other person

            found = False
            for i in range(size_array):

                if person[index + 1] == not_found:
                    if abs((people[i][index + 1][cmp['x']] - person[index][cmp['x']])) <= max_diff['x'] \
                            and abs((people[i][index + 1][cmp['y']] - person[index][cmp['y']])) <= max_diff['y'] \
                            and abs((people[i][index + 1][cmp['width']] - person[index][cmp['width']])) <= max_diff['width'] \
                            and abs((people[i][index + 1][cmp['height']] - person[index][cmp['height']])) <= max_diff['height']\
                            and person[index] != not_found:

                        # found that coordinate in an other person, so swap them
                        temp_coordinate = person[index + 1]
                        person[index + 1] = people[i][index + 1]
                        people[i][index + 1] = temp_coordinate
                        found = True
                        break

                    elif abs((last_coordinates[0] - people[i][index + 1][cmp['x']])) <= max_diff['x'] \
                            and abs((last_coordinates[1] - people[i][index + 1][cmp['y']])) <= max_diff['y'] \
                            and abs((last_coordinates[2] - people[i][index + 1][cmp['width']])) <= max_diff['width'] \
                            and abs((last_coordinates[3] - people[i][index + 1][cmp['height']])) <= max_diff['height'] \
                            and last_coordinates != [-1, -1, -1, -1]:

                        temp_coordinate = person[index + 1]
                        person[index + 1] = people[i][index + 1]
                        people[i][index + 1] = temp_coordinate
                        found = True
                        break

                else:   # else the manually put coordinate is the next coordinate
                    found = True
                    break


            gap_counter += 1

            if not found:  # set the last coordinate
                if gap_counter == 1:
                    last_coordinates = person[index]
                    interpolate_start = {'coordinate': last_coordinates, 'index': index + 1}


            elif gap_counter > 1:
                if gap_counter/FPS <= max_time_for_interpolating:  # Interpolating

                    x, y, width, height = interpolate_start['coordinate']

                    interpolate_end = {'coordinate': person[index + 1], 'index': index + 1}

                    x_diff = interpolate_end['coordinate'][cmp['x']] - interpolate_start['coordinate'][cmp['x']]
                    y_diff = interpolate_end['coordinate'][cmp['y']] - interpolate_start['coordinate'][cmp['y']]
                    width_diff = interpolate_end['coordinate'][cmp['width']] - interpolate_start['coordinate'][cmp['width']]
                    height_diff = interpolate_end['coordinate'][cmp['height']] - interpolate_start['coordinate'][cmp['height']]

                    for k, indx in enumerate(range(interpolate_start['index'], interpolate_end['index'])):

                        if x_diff != 0:
                            x = int(interpolate_start['coordinate'][cmp['x']] + (x_diff / gap_counter) * (k + 1))

                        if y_diff != 0:
                            y = int(interpolate_start['coordinate'][cmp['y']] + (y_diff / gap_counter) * (k + 1))

                        if width_diff != 0:
                            width = int(interpolate_start['coordinate'][cmp['width']] + (width_diff / gap_counter) * (k + 1))

                        if height_diff != 0:
                            height = int(interpolate_start['coordinate'][cmp['height']] + (height_diff / gap_counter) * (k + 1))

                        if x < 0 or y < 0 or width < 0 or height < 0:  # when there are some problems
                            print("THERE ARE SOME PROBLEMS IN INTERPOLATING!! The frame number is " + str(indx))
                            x = y = width = height = 0

                        person[indx] = [x, y, width, height]

                    gap_counter = 0
                    last_coordinates = [-1, -1, -1, -1]

                else:
                    gap_counter = 0
                    last_coordinates = [-1, -1, -1, -1]
            else:
                gap_counter = 0
                last_coordinates = [-1, -1, -1, -1]


# End of Sorting
#################

destination = destination + '/Sortierte Koordinaten 2.csv'

write_coordinates(people, size_array, destination)
