import cv2
import numpy as np
import mask
count = 0
cap = cv2.VideoCapture(0)


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
            # For every found contour we now apply approximation to polygons with 
            # accuracy +-0.02*peri and stating that the curve must be closed
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            center, radius = cv2.minEnclosingCircle(approx)
            # bounding boxes point set
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(outImg,(x,y,w,h),c,2)
            cv2.putText(outImg,"{}".format(letter),(x,y-10),cv2.FONT_HERSHEY_PLAIN,1.5,c,2)
            # cv2.circle(outImg,(int(center[0]),int(center[1])),int(radius),color,3)

# while True:
#     ret, frame = cap.read()
#     hsv = cv2.cvtColor(frame ,cv2.COLOR_BGR2HSV)
#     red = mask.rmask(hsv)
#     green = mask.gmask(hsv) 
#     getContour(red, frame,(0,0,255))
#     # getContour(green,frame)
#     cv2.imshow("result",rescale(frame,1.2))
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()