import csv
import sys


def read_coordinates(info_data, coordinates_data, with_fillers=False):
    """Reading the coordinates and the info_data so the info_data is a dictionary and the coordinates to access like:
        people[person_number][frame_number][x / y / width / height]

    :param info_data: path to the info_file
    :param coordinates_data: path to the coordinates_file
    :param with_fillers:
    :return: info file and coordinates of all people
    """

    # Reading the table
    with open(info_data, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            info = row

    number_of_person = int(info['number_of_person'])
    poss_wrong_det = int(info['poss_wrong_det'])

    if with_fillers:
        size_array = number_of_person + poss_wrong_det
    else:
        size_array = number_of_person

    people = []
    for i in range(size_array):
        people.append([])

    # reading the coordinates
    with open(coordinates_data, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            for number in range(size_array):
                splitted = row[number].strip('[]').split(',')
                people[number].append([int(splitted[i].strip()) for i in range(4)])

    return info, people


if __name__ == '__main__':
    if len(sys.argv[1:]) != 2:
        sys.stderr.write('Usage: readCoordinates.py <info_file> <coordinates_file>\n')
        sys.exit(1)
    else:
        read_coordinates(sys.argv[1], sys.argv[2])
