import os
import cv2
import csv
import sys
from mtcnn.mtcnn import MTCNN


# extract a single face from a given image
def detect_faces(frame, size_array, people, detector):
    detect_faces.counter += 1
    
    # detect faces in the image
    faces = detector.detect_faces(frame)
    
    # convert again into rgb
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    k = 0
    for results in faces:
        # confidence = '%.2f' % (results['confidence'] * 100)
        x1, y1, width, height = results['box']
        # x2, y2 = x1 + width, y1 + height
        
        # Creating the lables in the video
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # cv2.putText(frame, confidence, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Exporting the Coordinates
        coordinate = [x1, y1, width, height]
        people[k].append(coordinate)
        k += 1

    # If it doesn't find enough people, fill the others with not_found
    if len(faces) < size_array:
        for k in range(k, size_array):
            people[k].append(not_found)


    # cv2.putText(frame, "Frame: " + str(detect_faces.counter), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # output.write(frame)
    # cv2.namedWindow('Test', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('Test', frame)  # to preview the video
    # cv2.waitKey(1)


def write_in_file(size_array, frame_count, time_of_video, poss_wrong_det, number_of_person, source_path, FPS, people):
    # Creating the first table
    print("Writing into a csv file...")

    dir = 'outputs/'

    i = 0
    while os.path.exists(dir + 'Video ' + str(i)):
        i += 1

    dir = dir + 'Video ' + str(i)
    os.mkdir(dir)

    # Create the header
    header = []
    for number in range(size_array):
        person = "Person " + str(number + 1)
        header.append(person)

    zipped_people = zip(*people)

    with open(dir + '/Koordinaten.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in zipped_people:
            writer.writerow(row)

    # Creating the second table
    with open(dir + '/Info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['frame_count', 'time_of_video', 'poss_wrong_det', 'number_of_person', 'video_source', 'not_found', 'FPS'])
        writer.writerow([frame_count, time_of_video, poss_wrong_det, number_of_person, source_path, not_found, FPS])

    print("Finished!")


def main(args):
    if len(args) != 3:
        sys.stderr.write("Usage: FaceLabeler_GetLables.py <source> <number_of_person> <duration>")
        sys.exit(-1)

    # Variables
    source = args[0]  # videosource
    number_of_person = int(args[1])  # the number of person in the video
    duration = int(args[2])  # duration of the algorithm, 0 if full video

    # create the detector, using default weights
    detect_faces.counter = 0
    poss_wrong_det = int(number_of_person / 2) + 1  # the number of possible wrong detections (rather more than less)

    detector = MTCNN()
    people = []

    size_array = poss_wrong_det + number_of_person
    source_path = os.path.dirname(os.path.abspath(str(source))) + '/' + str(source)

    for i in range(0, size_array):
        people.append([])

    # Opening Camera/Video
    cap = cv2.VideoCapture(source)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)

    # frame_width = int(cap.get(3))
    # frame_height = int(cap.get(4))
    # output = cv2.VideoWriter('outputs/Labled Video.avi',
    # cv2.VideoWriter_fourcc('M', 'P', '4', '2'), 10, (frame_width, frame_height))

    curr_time = 0
    print("Start labeling...")
    while True:
        ret, frames = cap.read()
        if ret:
            frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
            if frames is None:
                print('--(!) No captured frame -- Break!')
                break

            detect_faces(frames, size_array, people, detector)

            # Display the time of the video
            curr_time = cap.get(cv2.CAP_PROP_POS_MSEC)
            print('Time: ' + str(round(curr_time, 2)) + ' milliseconds')

            # if cv2.waitKey(33) == ord('q'):
            #     break

            if 0 < duration <= curr_time:
                break

        else:
            break

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    
    time_of_video = (frame_count / FPS) * 1000 - (1 / FPS) * 1000

    # When everything done, release the video capture and the output
    cap.release()
    # output.release()
    # cv2.destroyAllWindows()

    write_in_file(size_array, frame_count, time_of_video, poss_wrong_det, number_of_person, source_path, FPS, people)


not_found = [0, 0, 0, 0]

if __name__ == '__main__':
    main(sys.argv[1:])
