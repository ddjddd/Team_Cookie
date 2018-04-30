import numpy as np
import cv2
from src import grid
# brown : 쿠키(투명해지는 범위까지 최대한 포함시키고자 했으나 투명해지는 부분에서 detection은 X)
brown_lower = np.array([10, 112, 210], np.uint8)
brown_upper = np.array([15, 180, 255], np.uint8)
kernel = np.ones((5, 5), "uint8")


def cookie(frame, cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h):
    global vertical_num, horizontal_num

    # frame을 HSV (hue-saturation-value)로 변환한다
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 해당 범위에 속하는 각 색깔을 찾는다

    brown = cv2.inRange(hsv, brown_lower, brown_upper)
    brown = cv2.dilate(brown, kernel)

    # transp - 투명해진 쿠키만 따로 범위를 뽑아냄
    transp_lower = np.array([2, 108, 143], np.uint8)
    transp_upper = np.array([16, 203, 201], np.uint8)

    # transp2 검은색 배경의 투명해진 쿠키.... ( 배경이 달라지면 trans3가 필요할 수 도 있음... )
    transp2_lower = np.array([7, 73, 94, ], np.uint8)
    transp2_upper = np.array([21, 189, 184, ], np.uint8)

    transp = cv2.inRange(hsv, transp_lower, transp_upper)
    transp2 = cv2.inRange(hsv, transp2_lower, transp2_upper)

    # dilate: morphology 연산 중 하나. 구조 요소를 사용하여 이웃한 화소들 중 최대 화소값으로 대체한다.
    # 즉, 어두운 영역이 줄어들며 밝은 영역이 늘어남. 노이즈 제거 후 줄어든 크기를 복구하고자 할 때 주로 사용.
    # bitwise_and 연산자는 둘다 0이 아닌 경우만 값을 통과 시킴.
    # 원본 이미지와 마스크 이미지를 AND 연산하여 노란색만 추출한다. 즉 mask 영역 이외는 모두 제거됨.

    transp = cv2.dilate(transp, kernel)
    transp2 = cv2.dilate(transp2, kernel)

    go = 1
    cookie_detected = False

    # cookie

    (_, contours, hierarchy) = cv2.findContours(brown, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 밤 때문에 가려지는 경우가 존재.
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        hierarchy_num = hierarchy[0][pic][-1]
        x, y, w, h = cv2.boundingRect(contour)
        if y < 400 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240) and hierarchy_num == -1:
            cookie_detected = True  # 투명한 쿠키를 디텍션할 필요 없음
            cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h = x, y, w, h  # 인식한 쿠키 좌표 저장
            cv2.rectangle(frame, (x, y), (x + w, y + h), (170, 100, 69), 5)

    # transp cookie
    if not cookie_detected:
        (_, contours, hierarchy) = cv2.findContours(transp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # hierarchy_num = hierarchy[0][pic][-1]
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if y < 400 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240):  # and hierarchy_num == -1:
                cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h = x, y, w, h
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cookie_detected = True

    # trnsp cookie 2
    elif not cookie_detected:
        (_, contours, hierarchy) = cv2.findContours(transp2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if y < 390 and 2000 < area and (200 < x + w / 2) and (
                    x + w / 2 < 240) and w < 100:  # and hierarchy_num == -1:
                cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h = x, y, w, h
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cookie_detected = True

    # 쿠키를 찾지 못하였을 때 전 프래임의 쿠키 위치를 그대로 사용
    if not cookie_detected:
        x, y, w, h = cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h



    return cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_y
