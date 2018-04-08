import cv2
import numpy as np
cap = cv2.VideoCapture("cookierun.mp4")
#image = cv2.imread("obstacle1.jpg")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
cv2.namedWindow('canny')

def nothing(x):
    pass

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
# add lower and upper threshold slidebars to "canny"
cv2.createTrackbar('lower', 'canny', 0, 255, nothing)
cv2.createTrackbar('upper', 'canny', 0, 255, nothing)


#hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
while(1):
    ret, frame = cap.read()
    b_frame=cv2.GaussianBlur(frame, (5,5), 0)

    # 색추출
    hsv = cv2.cvtColor(b_frame, cv2.COLOR_BGR2HSV)
    yellow_lower = np.array([9, 147, 122], np.uint8)
    yellow_upper = np.array([76, 255, 255], np.uint8)

    pink_lower = np.array([169, 96, 220], np.uint8)
    pink_upper = np.array([174, 140, 255], np.uint8)

    blue_lower = np.array([40, 79, 79], np.uint8)
    blue_upper = np.array([134, 243, 255], np.uint8)

    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    yellow_inv = cv2.bitwise_not(yellow)  # 노랑만 검정
    pink = cv2.inRange(hsv, pink_lower, pink_upper)
    pink_inv = cv2.bitwise_not(pink)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    blue_inv = cv2.bitwise_not(blue)

    remove = yellow_inv & pink_inv & blue_inv
    res = cv2.bitwise_and(b_frame, b_frame, mask=remove)

    #배경 삭제
    fgmask = fgbg.apply(res)
    fgmask=cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    combine=cv2.bitwise_and(b_frame, b_frame, mask=fgmask)
    combine=combine&res

    cv2.imshow('frame', combine)

    # threshold bar에서 값 추출
    l_t = cv2.getTrackbarPos('lower', 'canny')
    u_t = cv2.getTrackbarPos('upper', 'canny')
    s = cv2.getTrackbarPos(switch, 'canny')

    if s == 0:
        edges = combine
    else:
        edges = cv2.Canny(combine, l_t, u_t)
        edges = cv2.dilate(edges, None, iterations=1)

    # display images
    cv2.imshow('original', combine)
    cv2.imshow('canny', edges)

    '''
    gray=cv2.cvtColor(combine, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)

    mov, contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mov=cv2.drawContours(combine, contours, -1, (0, 255, 0), 2)
    '''
    cv2.imshow('final', edges)
    k=cv2.waitKey(30)&0xff
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()


