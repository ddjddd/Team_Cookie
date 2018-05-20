################################
################################
# 모듈명    : obstacles_and_jelly
# 작성자    : 최진호
# 설명      : 플레이 화면에서 장애물과 젤리를 인식하고 리스트에 저장
################################
################################

import cv2
from src import image_filter as imf
from src import window_size as ws


################################
# 함수명    : make_obstacle_list
# 작성자    : 최진호
# 설명      : 인접한 장애물 개체를 하나로 병합
# 리턴      : _
# 매개변수  : list obstacle_list 병합된 장애물 리스트
################################
def make_obstacle_list(obstacle_list):
    obstacle_list.sort()

    # 검출된 장애물 리스트 하나하나 검사
    for i in range(len(obstacle_list)):
        j = i + 1
        while j < len(obstacle_list):
            merge = False

            # x 좌표가 겹칠 경우에 검사
            if obstacle_list[i][2] >= obstacle_list[j][0]:
                if obstacle_list[i][1] <= obstacle_list[j][1] <= obstacle_list[i][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][3] = max(obstacle_list[i][3], obstacle_list[j][3])
                    del obstacle_list[j]    # j 번째 개체를 i와 합친다
                    merge = True
                elif obstacle_list[i][1] <= obstacle_list[j][3] <= obstacle_list[i][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][1] = min(obstacle_list[i][1], obstacle_list[j][1])
                    del obstacle_list[j]    # j 번째 개체를 i와 합친다
                    merge = True
                elif obstacle_list[i][1] >= obstacle_list[j][1] and obstacle_list[i][3] <= obstacle_list[j][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][1] = obstacle_list[j][1]
                    obstacle_list[i][3] = obstacle_list[j][3]
                    del obstacle_list[j]    # j 번째 개체를 i와 합친다
                    merge = True

            # 병합되지 않은 경우 경우 다음 개체 검사
            if merge is False:
                j += 1
            # 병합된 경우 처음부터 다시 검사
            else:
                j = i + 1


################################
# 함수명    : obstacle_and_jelly
# 작성자    : 최진호
# 설명      : 플레이 윈도우 화면에서 장애물, 젤리 오브젝트 검출
# 리턴      : list obstacle_list 검출된 장애물 개체 리스트
#             list jelly_list 검출된 젤리 개체 리스트
# 매개변수  : image play_frame 분활된 플레이 화면
################################
def obstacle_and_jelly(play_frame):
    play_canny = imf.make_canny(play_frame)
    object_list = []

    # 모든 윤곽선 검출
    _, roi_contours, roi_hierarchy = cv2.findContours(play_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] == -1:
            if rect_area >= 550:
                object_list.append([x + ws.wx1, y + ws.wy1, x + ws.wx1 + w, y + ws.wy1 + h])

    make_obstacle_list(object_list)

    obstacle_list = []
    jelly_list = []
    for i in range(len(object_list)):
        x, y, w, h = object_list[i]
        # 상단 장애물
        if y <= ws.wy1 + 10:
            obstacle_list.append(object_list[i])
        # 하단 장애물
        elif h >= ws.wy2 - 15:
            obstacle_list.append(object_list[i])
        # 장애물이 아니면 전부 젤리
        else:
            jelly_list.append(object_list[i])

    return obstacle_list, jelly_list
