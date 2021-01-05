"""Scale the coordinates again to 4k after resized the video to FHD."""

import sys
import numpy as np

from readCoordinates import read_coordinates
from writeCoordinates import write_coordinates


def main(args):

    if len(args) != 3:
        sys.stderr.write('Usage: scaleCoordinates.py <info_file> <coordinates_file> <destination>\n')
        sys.exit(1)

    info_file = args[0]
    coordinates_file = args[1]
    destination = args[2]

    info, people = read_coordinates(info_file, coordinates_file)

    people = np.array(people) * 2
    people = people.tolist()

    size_array = int(info['number_of_person'])
    write_coordinates(people, size_array, destination)


if __name__ == '__main__':
    main(sys.argv[1:])
