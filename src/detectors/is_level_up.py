import cv2
import numpy as np
import time

def islevelup(img,inputtime):

    window_y, window_x, _ = img.shape  # 화면의 크기
    x_unit = int(window_x /40)
    y_unit = int(window_y/40)

    #래벨 업 글자 범위
    letter = img[y_unit*7 : y_unit*10 , x_unit*18 : x_unit*24] # 외부에서 작제 잘라서 줘도 됨

    #빈 공간 아무데나 범위
    empty = img[y_unit * 5: y_unit * 5+1, x_unit * 18: x_unit * 24] # 외부에서 작제 잘라서 줘도 됨


    # 글자 색 디텍트
    kernel = np.ones((20, 20), "uint8")
    letter = cv2.dilate(letter, kernel)
    letter_low = np.array([0, 0, 240], np.uint8)
    letter_high = np.array([100, 40, 255], np.uint8)
    hsv = cv2.cvtColor(letter, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,letter_low , letter_high)
    letter = cv2.bitwise_and(letter, letter, mask=mask)


    cv2.imshow('letter', letter)
    lettersum= 0
    emptysum = 0

    xlength = letter.shape[1]
    ylength = letter.shape[0]
    ycenter = int(ylength / 2)

    threshold = 210
    threshold2 = 30
    current = time.time()
    for i in range(xlength):
        lettersum += sum(letter[ycenter, i])
        emptysum += sum(empty[0,i])
    if lettersum/i > threshold and emptysum/i < threshold2 and current-inputtime > 5 : # 글자부분은 하얗고, 다른 공간은 까맣고, 전 레벨업 부터 5초 이상 지났을 때
        return True

    # cv2.imshow('letter_original2', empty)
    # cv2.imshow('letter_original', image)

    #scale=10
    #image= cv2.resize(image, None, fx=1/scale, fy=1/scale)
    #image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    return False
