import cv2
import numpy as np

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

lower_blue = np.array([90, 100, 100])
upper_blue = np.array([130, 255, 255])

lower_green = np.array([40, 40, 40]) 
upper_green = np.array([70, 255, 255]) 

def rmask(hsv):
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    return cv2.bitwise_or(red_mask1, red_mask2)

def bmask(hsv):
    return cv2.inRange(hsv, lower_blue, upper_blue)

def gmask(hsv):
    return cv2.inRange(hsv,lower_green,upper_green)

