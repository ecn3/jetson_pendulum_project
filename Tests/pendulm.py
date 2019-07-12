import numpy as np
import cv2 as cv
import math

cap = cv.VideoCapture("/dev/video1") # set video to use usb camera


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here, set color to normal
    color = cv.cvtColor(frame, cv.WINDOW_NORMAL) 

    # Display the resulting frame
    cv.imshow('frame',color)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
