"""Exports all the faces in a video file that are detected."""

import cv2
import numpy as np
import sys
from readCoordinates import read_coordinates
from PIL import Image
import os


class Info:
    def __init__(self, FPS, not_found, number_of_person, size_array, people, video_file, duration, height, width, resolution, destination, max_frame, cap, bigger_bounding=False, extra_width=0, extra_height=0):
        self.FPS = FPS
        self.max_frame = max_frame
        self.not_found = not_found
        self.number_of_person = number_of_person
        self.size_array = size_array
        self.people = people
        self.video_file = video_file
        self.duration = duration
        self.height = height
        self.width = width
        self.resolution = resolution
        self.destination = destination
        self.cap = cap
        self.bigger_bounding = bigger_bounding
        self.extra_width = extra_width
        self.extra_height = extra_height


def initialize(info_data, coordinates_data, destination, with_fillers, height, width, resolution, duration, bigger_bounding=False, extra_width=0, extra_height=0):

    info, people = read_coordinates(info_data, coordinates_data, with_fillers=with_fillers)

    not_found_temp = info['not_found'].strip('[]').split(', ')
    not_found = ([int(not_found_temp[i]) for i in range(4)])
    number_of_person = int(info['number_of_person'])
    poss_wrong_det = int(info['poss_wrong_det'])

    if with_fillers:
        size_array = number_of_person + poss_wrong_det
    else:
        size_array = number_of_person

    video_file = info['video_source']
    FPS = float(info['FPS'])


    # open the video file

    cap = cv2.VideoCapture(video_file)
    if not (cap.isOpened or os.path.exists(video_file)):
        print('--(!)Error opening video capture')
        exit(0)


    if duration > 0:
        max_frame = int((duration / 1000) * FPS)
    else:
        max_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


    info = Info(FPS, not_found, number_of_person, size_array, people, video_file, duration, height, width, resolution, destination, max_frame, cap, bigger_bounding=bigger_bounding, extra_height=extra_height, extra_width=extra_width)

    return info


def extract_faces(frame, frame_num, info):

    faces = crop_faces(frame, frame_num-1, info)
    extract_faces.rows.append(make_row(faces, frame_num, info))
    print(frame_num)

    if len(extract_faces.rows) >= int(info.resolution['y'] / info.height) or frame_num == info.max_frame:
        extract_faces.columns.append(np.vstack(extract_faces.rows[:]))
        extract_faces.rows = []

        if len(extract_faces.columns) >= int(info.resolution['x'] / (info.width*info.size_array)) or frame_num == info.max_frame:

            if frame_num == info.max_frame:
                extract_faces.columns[-1] = cv2.resize(extract_faces.columns[-1], (extract_faces.columns[0].shape[1], extract_faces.columns[0].shape[0]))

            pic = np.hstack(extract_faces.columns[:])

            extract_faces.columns = []

            # save pic

            im = Image.fromarray(cv2.cvtColor(pic, cv2.COLOR_BGR2RGB))
            im.save(info.destination + "/Bild " + str(extract_faces.counter) + ".jpeg")
            extract_faces.counter += 1

            return pic

extract_faces.rows = []
extract_faces.columns = []
extract_faces.counter = 0


def write_frame_count(row, frame_num, info):

    img = np.zeros((info.height, info.width*2, 3), dtype=np.uint8)
    img.fill(0)

    cv2.putText(img, str(frame_num), (10, int(info.height/2 + 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    row_with_count = np.hstack([img, row])

    return row_with_count


def crop_faces(frame, frame_num, info):
    faces = []

    for person_count, person in enumerate(info.people):

        if info.bigger_bounding:
            x = person[frame_num][0] - info.extra_width
            y = person[frame_num][1] - info.extra_height
            width = person[frame_num][2] + 2 * info.extra_width
            height = person[frame_num][3] + 2 * info.extra_height

            # proof whether the coordinates are in the frames or not
            if x < 0: x = 0
            if y < 0: y = 0


        else:
            x = person[frame_num][0]
            y = person[frame_num][1]
            width = person[frame_num][2]
            height = person[frame_num][3]

        if person[frame_num] == info.not_found and person_count >= info.number_of_person:
            img = np.zeros((1, 1, 3), dtype=np.uint8)
            img.fill(50)
            faces.append(img)

        elif person[frame_num] == info.not_found and person_count < info.number_of_person:
            img = np.zeros((1, 1, 3), dtype=np.uint8)
            img.fill(150)
            faces.append(img)

        else:
            faces.append(frame[y:y + height, x:x + width])

    return faces


def make_row(faces, frame_num, info):

    for img_num in range(info.size_array):
        faces[img_num] = cv2.resize(faces[img_num], (info.width, info.height))

    row = np.hstack(faces[:])

    return write_frame_count(row, frame_num, info)


def main(args):

    if len(args) != 5:
        sys.stderr.write('Usage: getFaces.py <info_file> <coordinates_file> <destination> <with_fillers> <duration>\n')
        sys.exit(1)

    info_file = args[0]
    coordinates_file = args[1]
    destination = args[2]
    with_fillers = int(args[3])
    duration = int(args[4])
    height = 150
    width = 100
    resolution = {'x': width * 4 * 15, 'y': height * 30}    # width * (number_of_person + 1) * number_of_columns
                                                            # height * number_of_rows

    info = initialize(info_file, coordinates_file, destination, with_fillers, height, width, resolution, duration)

    time_of_video = 0

    ## Start the loop ##

    while True:
        ret, frames = info.cap.read()
        if ret:
            if frames is None:
                print('--(!) No captured frame -- Break!')
                break

            extract_faces(frames, int(info.cap.get(cv2.CAP_PROP_POS_FRAMES)), info)

            cap_time = info.cap.get(cv2.CAP_PROP_POS_MSEC)
            if cap_time != 0.0:
                time_of_video = cap_time

            print('Time: ' + str(round(time_of_video/1000, 2)) + ' seconds')

            if 0 < info.duration <= cap_time:
                break

        else:
            break

    info.cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1:])
