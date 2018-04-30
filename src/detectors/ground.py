import cv2
from src import image_filter as imf, window_size as ws
from src.detectors import collision_detector as cd


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


# 바닥 오브젝트를 검출
def ground(frame, hgt, wth):
    # 바닥 화면만을 우선적으로 검사
    gx1, gx2, gy1, gy2 = ws.get_ground_size(hgt, wth)
    ground_frame = frame[gy1:gy2, gx1:gx2]
    binary = imf.make_canny(ground_frame)

    # 외곽선 검출
    _, contours, roi_hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ground_list = []
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] is not -1:
            if rect_area >= 250:
                ground_list.append([x+gx1, y+gy1, x+w+gx1, y+h+gy1])

    make_ground_list(ground_list)           # 인접한 바닥 오브젝트 묶기


    # 사각형 그리는 함수    # 현재 비활성화
    # for i in range(len(ground_list)):
    #     x, y, w, h = ground_list[i]
    #     cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 2)

    cd.ground_collision(frame, ground_list)     # 바닥-그리드 충돌 검사 및 그리드 채우기

    return
