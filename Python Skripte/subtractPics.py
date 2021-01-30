import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2


def main(args):
    path = "inputs1/Lips.avi"
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        sys.exit("Cap is not opened")

    while cap.isOpened():
        _, first_frame = cap.read()
        _, second_frame = cap.read()

        first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
        second_frame = cv2.cvtColor(second_frame, cv2.COLOR_BGR2RGB)

        diff = second_frame - first_frame

        plt.subplot(1, 3, 1)
        plt.imshow(first_frame)
        plt.subplot(1, 3, 2)
        plt.imshow(second_frame)
        plt.subplot(1, 3, 3)
        plt.imshow(diff)
        plt.colorbar()

        plt.show()


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1:])


