import cv2
import serial
import time
from PyQt5 import  QtWidgets
count = 0
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=0.1)
global value
value = "0"

def write_data(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.06)
    data = arduino.readline()
    return data

def rescale(frame, scale = 0.2):
    w = int(frame.shape[1]*scale)
    h = int(frame.shape[0]*scale)
    dim = (w,h)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def getContour(inImg,outImg,c = (0,0,0),letter=""):
    contour, _ = cv2.findContours(inImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 1000:
            if(letter == "red"):
                write_data("1")
                # value = "0"
            if(letter == "green"):
                write_data("2")
                # value = "0"
            if(letter == "yellow"):
                write_data("3")
                # value = "0"
            # For every found contour we now apply approximation to polygons with 
            # accuracy +-0.02*peri and stating that the curve must be closed
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # center, radius = cv2.minEnclosingCircle(approx)
            # bounding boxes point set
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(outImg,(x,y,w,h),c,2)
            cv2.putText(outImg,"{}".format(letter),(x,y-10),cv2.FONT_HERSHEY_PLAIN,1.5,c,2)
            if cv2.countNonZero(inImg) > 0 :
                # print(letter)
                return letter


