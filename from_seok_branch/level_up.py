# importing modules

import cv2
import numpy as np

# capturing video through webcam
cap = cv2.VideoCapture("cookierun.mp4")

go=1

def islevelup(image,start):

    window_y, window_x, _ = image.shape  # 화면의 크기
    x_unit = int(window_x /40)
    y_unit = int(window_y/41)
    #래벨 업 글자 범위
    image = image[y_unit*7 : y_unit*10 , x_unit*18 : x_unit*23]
    cv2.imshow('letter_original', image)


    # 글자 색 디텍트
    kernel = np.ones((20, 20), "uint8")
    image = cv2.dilate(image, kernel)
    letter_low = np.array([0, 0, 240], np.uint8)
    letter_high = np.array([100, 40, 255], np.uint8)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,letter_low , letter_high)

    image = cv2.bitwise_and(image, image, mask=mask)

    scale=10
    image= cv2.resize(image, None, fx=1/scale, fy=1/scale)
    image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    cv2.imshow('letter', image)
    pixelsumx = 0
    pixelsumy = 0

    xlength = image.shape[1]
    xcenter = int(xlength/2)
    ylength = image.shape[0]
    ycenter = int(ylength / 2)

    threshold = 210
    threshold2 = 80
    i=0
    while i < xlength :
        pixelsumx += sum(image[ycenter, i])
        i+=1
    j = 0
    while j < ylength:
        pixelsumy += sum(image[j, xcenter])
        j += 1
    print(pixelsumy/j/3)
    if start and pixelsumx/i/3 > threshold and pixelsumy/j/3> threshold : # 범위 내 흰색(글자의 색)이 대부분일 것으로 추정 = 레벨 업 합
        return True
    if not start and pixelsumx/i/3 < threshold2 and pixelsumy/j/3 < threshold2 : # 범위 내 흰색(글자의 색)이 대부분일 것으로 추정 = 레벨 업 합
        return True

    return False
levelupflag = 0
ret, frame = cap.read()
while (ret):
    go=1


    if islevelup(frame,1):
        levelupflag = 1
        cv2.putText(frame, "level up!", org=(100, 300), fontFace=1, fontScale=10, color=(255, 0, 0), thickness=5)
    if levelupflag and islevelup(frame,0):
        levelupflag = 0



    cv2.imshow("Color Tracking", frame)
    #cv2.imshow("letter", range)
    if cv2.waitKey(go) & 0xFF == ord('q'):
        break

    ret, frame = cap.read()


cap.release()
cv2.destroyAllWindows()

