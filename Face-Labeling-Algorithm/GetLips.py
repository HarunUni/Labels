import os
import cv2
import csv
import sys
import numpy as np
from moviepy.editor import *

from mtcnn.mtcnn import MTCNN


# extract a single face from a given image
def detect_faces(frame, detector, output, lip_height):
    detect_faces.counter += 1
    lip_width = 120

    try:
        # detect faces in the image
        face = detector.detect_faces(frame)[0]
        keypoints = face['keypoints']
        mouth_left = keypoints['mouth_left']
        mouth_right = keypoints['mouth_right']

        # convert again into rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Creating the lables in the video
        # cv2.rectangle(frame, (mouth_left[0], mouth_left[1] - 20), (mouth_right[0], mouth_right[1] + 20), (0, 0, 255), 2)

        # Exporting the Coordinates
        # coordinate = [x1, y1, width, height]


        # cv2.putText(frame, "Frame: " + str(detect_faces.counter), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        frame = frame[(mouth_left[1] - int(lip_height/2)):(mouth_right[1] + int(lip_height/2)), mouth_left[0]:mouth_right[0]]
        frame = cv2.resize(frame, (lip_width, lip_height))
    except:
        frame = np.ones((lip_width, lip_height, 3), dtype=np.uint8)

    finally:
        output.write(frame)
        # cv2.namedWindow('Test', cv2.WINDOW_KEEPRATIO)
        # cv2.imshow('Test', frame)  # to preview the video
        # cv2.waitKey(30)


def main(args):
    if len(args) != 3:
        sys.stderr.write("Usage: FaceLabeler_GetLables.py <source> <lip_height> <duration>")
        sys.exit(-1)

    # Variables
    source = args[0]  # videosource
    lip_height = int(args[1])
    duration = int(args[2])  # duration of the algorithm, 0 if full video

    detector = MTCNN()

    source_path = os.path.dirname(os.path.abspath(str(source))) + '/' + str(source)

    # Opening Camera/Video
    cap = cv2.VideoCapture(source)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)

    frame_width = int(cap.get(3))
    output = cv2.VideoWriter('outputs/Lips.avi',
                             cv2.VideoWriter_fourcc('M', 'P', '4', '2'), 29.97, (120, lip_height))
    frame_height = int(cap.get(4))

    curr_time = 0
    detect_faces.counter = 0
    print("Start labeling...")
    while True:
        ret, frames = cap.read()
        if ret:
            frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

            if frames is None:
                print('--(!) No captured frame -- Break!')
                break

            detect_faces(frames, detector, output, lip_height)

            # Display the time of the video
            curr_time = cap.get(cv2.CAP_PROP_POS_MSEC)
            print('Time: ' + str(round(curr_time, 2)) + ' milliseconds')

            # if cv2.waitKey(33) == ord('q'):
            #     break

            if 0 < duration <= curr_time:
                break

        else:
            break

    # When everything done, release the video capture and the output
    cap.release()
    output.release()
    cv2.destroyAllWindows()

    audioclip = AudioFileClip('input/Audio.wav')
    audioclip = audioclip.subclip(t_start=0, t_end=20)
    videoclip = VideoFileClip('outputs/Lips.avi')
    videoclip = videoclip.set_audio(audioclip)

    videoclip.write_videofile('outputs/Lips with Audio.mp4')


not_found = [0, 0, 0, 0]

if __name__ == '__main__':
    main(sys.argv[1:])
