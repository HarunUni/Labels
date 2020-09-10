import sys
import cv2
import moviepy.editor as mpy
from readCoordinates import read_coordinates
import pandas as pd


def draw_labels(frame, coordinates, info, frame_count, VAD):
    for person in range(int(info['number_of_person'])):
        x1, y1, width, height = coordinates[person][frame_count]
        x2 = x1 + width
        y2 = y1 + height

        # Determine the color of the label: if there is speech, it is green, if not, it is red
        if VAD[frame_count]:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    return frame


def save_video(audio, destination, path_without_audio):

    path_with_audio = destination + "/video with audio.mp4"

    print("Writing video with audio")

    video = mpy.VideoFileClip(path_without_audio)
    video = video.set_audio(audio)
    video.write_videofile(path_with_audio)


def open_video(video_source):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print('--(!)Error opening video capture')
        exit(0)

    return cap


def main(args):
    if len(args) != 4:
        sys.stderr.write("Usage: drawLabels.py <info file> <coordinates file> <destination> <duration in ms>")
        sys.exit(-1)

    # Initialization
    info_file = args[0]
    coordinates_file = args[1]
    destination = args[2]
    duration = int(args[3])

    info, coordinates = read_coordinates(info_file, coordinates_file)
    VAD = list(pd.read_csv(coordinates_file)['VAD'])
    cap = open_video(info['video_source'])
    audio = mpy.AudioFileClip(info['video_source'])
    frame_count = 0

    # Preparing the video without audio
    path_without_audio = destination + "/video without audio.avi"
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(path_without_audio, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (width, height))

    "Go through the whole video"
    while True:
        ret, frame = cap.read()
        if ret:
            if frame is None:
                print('--(!) No captured frame -- Break!')
                break

            frame = draw_labels(frame, coordinates, info, frame_count, VAD)
            frame_count = frame_count + 1

            print("Frame: " + str(frame_count))
            curr_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            out.write(frame)

            if 0 < duration <= curr_time:
                break

        else:
            break


    print("Writing video without audio")
    out.release()

    save_video(audio, destination, path_without_audio)



if __name__ == '__main__':
    main(sys.argv[1:])
