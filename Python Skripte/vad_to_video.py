"""Show the vad's.

Draw a circle into a video that shows the vad activity and put the audio in the background. The difference to `drawLabels.py` is that this does not draw the labels.
"""

import pandas as pd
import cv2
import moviepy.editor as mpy
import sys


def write_vad(frame, vad):

    thickness = -1
    center = (120, 120)
    radius = 120
    
    if vad:
        color = (0, 255, 0)
    else:
        color = (0, 0, 255)

    frame = cv2.circle(frame, center, radius, color, thickness)

    return frame


def save_video(path_without_audio, audio_path):

    print("Writing video with audio...")
    path_with_audio = path_without_audio.split('.', 1)[0] + "_with_audio.mp4"

    video = mpy.VideoFileClip(path_without_audio)
    audio = mpy.AudioFileClip(audio_path)
    video2 = video.set_audio(audio)
    video2.write_videofile(path_with_audio)


def main(args):

    video_path = args[0]
    vad_path = args[1]
    audio_path = args[2]
    output_filename = args[3]

    # open files
    vad = pd.read_csv(vad_path)
    cap = cv2.VideoCapture(video_path)
    end_second = float(vad.iloc[-1, -1])
    second = 0

    # open video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    row = 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create the output video
    output = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'MJPG'), fps, (int(width), int(height)))

    while ret:
        
        vad_label, _, to_sec = vad.iloc[row]
        
        # go through that row of the vad file
        while second <= to_sec and ret:

            frame_out = write_vad(frame, vad_label)
            ret, frame = cap.read()
            output.write(frame_out)
            second = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            print("Second: " + str(second))

        row += 1
        print("Row: " + str(row))
        
        if second >= end_second:
            ret = False

    output.release()
    cap.release()

    save_video(output_filename, audio_path)


if __name__ == '__main__':
    main(sys.argv[1:]) 
