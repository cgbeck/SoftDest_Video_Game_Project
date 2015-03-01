import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v=0,52,100
# h,s,v = 100,100,100
# h,s,v=108,110,95
# h,s,v=0,196,161
# Creating track bar
# cv2.createTrackbar('h', 'result',0,179,nothing)
# cv2.createTrackbar('s', 'result',0,255,nothing)
# cv2.createTrackbar('v', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    # h = cv2.getTrackbarPos('h','result')
    # s = cv2.getTrackbarPos('s','result')
    # v = cv2.getTrackbarPos('v','result')
#108,110,95
    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([180,255,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(result,kernel,iterations = 3)
    kernel = np.ones((1,1),np.uint8)
    dilation = cv2.dilate(erosion,kernel,iterations =1)

    gray = cv2.cvtColor(dilation, cv2.COLOR_BGR2GRAY)
    # gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY_INV, 11, 1)
    cont_img = gray.copy()
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    

    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    #Finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.drawContours(frame,best_cnt,0, (128,255,0), 3)
    cv2.circle(frame,(cx,cy),15,(0,0,255),-1)
    cv2.rectangle(frame,(cx-80,cy-150),(cx+80,cy+150),(0,255,255),4)
    cv2.imshow('process', gray)
    cv2.imshow('result',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
            break

cap.release()

cv2.destroyAllWindows()