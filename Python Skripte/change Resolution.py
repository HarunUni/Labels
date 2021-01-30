"""Resize the resolution of the video to 1920x960."""

import cv2
import numpy as np
import sys
 
cap = cv2.VideoCapture(sys.argv[1])
FPS = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, FPS, (1920,960))
 
while True:
    ret, frame = cap.read()
    if ret:
        b = cv2.resize(frame,(1920,960),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
        
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
print("Finished")
