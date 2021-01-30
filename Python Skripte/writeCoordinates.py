"""Writes the coordinates to a file."""
import csv


def write_coordinates(people, size_array, destination):

    print("Writing into a csv file...")

    zipped_people = zip(*people)

    # Create the header
    header = []
    for number in range(size_array):
        person = "Person " + str(number + 1)
        header.append(person)

    with open(destination, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in zipped_people:
            writer.writerow(row)
