################################
################################
# 모듈명    : ground
# 작성자    : 최진호
# 설명      : 분할된 바닥 화면에서 바닥 인식 및 병합 후 리스트에 저장
################################
################################

import cv2
from src import image_filter as imf
from src import window_size as ws


################################
# 함수명    : make_ground_list
# 작성자    : 최재필
# 설명      : 인접한 바닥 개체를 하나로 병합
# 리턴      : _
# 매개변수  : list ground_list 검출된 바닥 리스트
################################
# 인접한 오브젝트를 묶어 하나의 오브젝트로 만든다
def make_ground_list(ground_list):
    ground_list.sort()
    thr = 40
    for i in range(len(ground_list)):
        j = i + 1
        while j < len(ground_list):
            merge = False
            if ground_list[i][2] + thr >= ground_list[j][0] >= ground_list[i][2]:
                ground_list[i][1] = min(ground_list[i][1], ground_list[j][1])
                ground_list[i][2] = ground_list[j][2]
                del ground_list[j]
                merge = True

            if merge is False:
                j += 1
            else:
                j = i + 1


################################
# 함수명    : ground
# 작성자    : 최재필
# 설명      : 분할된 바닥 화면에서 바닥 개체 검출
# 리턴      : list ground_list 검출된 바닥 리스트
# 매개변수  : image ground_frame 분할된 바닥 화면
################################
def ground(ground_frame):
    binary = imf.make_canny(ground_frame) # 화면 필터링

    # 윤곽선 검출
    _, contours, roi_hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ground_list = []
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] is not -1:
            if rect_area >= 250:
                ground_list.append([x+ws.gx1, y+ws.gy1, x+w+ws.gx1, y+h+ws.gy1])

    make_ground_list(ground_list)           # 인접한 바닥 오브젝트 묶기

    return ground_list
