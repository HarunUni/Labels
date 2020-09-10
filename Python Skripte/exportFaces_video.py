import cv2
import getFaces
import sys


def save_faces(picture, info, videos):

    height, width, _ = picture.shape

    rows = int(height / info.height)
    width_col = info.width * (2 + info.number_of_person)
    columns = int(width / width_col)

    for column in range(columns):
        for person in range(info.number_of_person):
            for row in range(rows):
                x_pers = info.width * (2 + person) + column * width_col
                y_pers = info.height * row
                videos[person].write(picture[y_pers:(y_pers + info.height - 1), x_pers:(x_pers + info.width - 1)])
                # Display the resulting frame
                # cv2.imshow('Frame', picture[y_pers:(y_pers + info.height), x_pers:(x_pers + info.width)])
                # cv2.waitKey(20)
                
        
def main(args):
    
    if len(args) != 3:
        sys.stderr.write('Usage: exportFaces_video.py <info_file> <coordinates_file> <destination>\n')
        sys.exit(1)
    
    info_file = args[0]
    coordinates_file = args[1]
    destination = args[2]
    height = 600
    width = 400
    resolution = {'x': width * 9 * 5, 'y': height * 25}
    duration = 20000
    extra_width = 30
    extra_height = 30
    bigger_bounding = True

    info = getFaces.initialize(info_file, coordinates_file, destination, False, height, width, resolution, duration, bigger_bounding=bigger_bounding, extra_height=extra_height, extra_width=extra_width)


    if not info.cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)


    videos = []

    for vid in range(info.number_of_person):
        output = cv2.VideoWriter(destination + "/Person " + str(vid) + ".avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (info.width-1, info.height-1))
        videos.append(output)


    while True:
        ret, frame = info.cap.read()

        if ret:

            if frame is None:
                print('--(!) No captured frame -- Break!')
                break

            pic = getFaces.extract_faces(frame, int(info.cap.get(cv2.CAP_PROP_POS_FRAMES)), info)

            if pic is not None:
                save_faces(pic, info, videos)
                pic = None

            cap_time = info.cap.get(cv2.CAP_PROP_POS_MSEC)

            if 0 < info.duration <= cap_time:
                break

        else:
            break

    info.cap.release()
    cv2.destroyAllWindows()
    
    for i in range(info.number_of_person):
        videos[i].release()


if __name__ == '__main__':
    main(sys.argv[1:])
