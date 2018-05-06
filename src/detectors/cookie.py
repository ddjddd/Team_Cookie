import numpy as np
import cv2
from src import window_size as ws

# brown : 쿠키(투명해지는 범위까지 최대한 포함시키고자 했으나 투명해지는 부분에서 detection은 X)
brown_lower = np.array([10, 112, 210], np.uint8)
brown_upper = np.array([15, 180, 255], np.uint8)
kernel = np.ones((5, 5), "uint8")


def cookie(cookie_frame, save_x, save_y, save_w, save_h):
    # frame 을 HSV (hue-saturation-value)로 변환한다
    hsv = cv2.cvtColor(cookie_frame, cv2.COLOR_BGR2HSV)

    # 해당 범위에 속하는 갈색을 찾는다
    brown = cv2.inRange(hsv, brown_lower, brown_upper)
    brown = cv2.dilate(brown, kernel)

    # trans - 투명해진 쿠키만 따로 범위를 뽑아냄
    trans_lower = np.array([2, 108, 143], np.uint8)
    trans_upper = np.array([16, 203, 201], np.uint8)
    trans = cv2.inRange(hsv, trans_lower, trans_upper)
    trans = cv2.dilate(trans, kernel)

    cookie_detected = False
    # 일반적인 상황에서 쿠키 검출
    _, contours, hierarchy = cv2.findContours(brown, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 밤 때문에 가려지는 경우가 존재.
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        hierarchy_num = hierarchy[0][pic][-1]
        x, y, w, h = cv2.boundingRect(contour)
        x += ws.cx1
        if y < 400 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240) and hierarchy_num == -1:
            cookie_detected = True          # 투명한 쿠키를 디텍션할 필요 없음
            save_x, save_y, save_w, save_h = x, y, w, h     # 인식한 쿠키 좌표 저장
            # cv2.rectangle(cookie_frame, (x, y), (x + w, y + h), (170, 100, 69), 5)

    # 일반 쿠키가 미검출 시 투명화된 쿠키 검출
    if not cookie_detected:
        _, contours, _ = cv2.findContours(trans, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            x += ws.cx1
            if y < 400 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240):
                save_x, save_y, save_w, save_h = x, y, w, h

    # 쿠키를 찾지 못하였을 때 전 프레임의 쿠키 위치를 그대로 사용
    return save_x, save_y, save_w, save_h
