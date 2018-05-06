import cv2
from src import image_filter as imf
from src import window_size as ws


def make_obstacle_list(obstacle_list):
    obstacle_list.sort()
    for i in range(len(obstacle_list)):
        j = i + 1
        while j < len(obstacle_list):
            merge = False
            if obstacle_list[i][2] >= obstacle_list[j][0]:
                if obstacle_list[i][1] <= obstacle_list[j][1] <= obstacle_list[i][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][3] = max(obstacle_list[i][3], obstacle_list[j][3])
                    del obstacle_list[j]
                    merge = True
                elif obstacle_list[i][1] <= obstacle_list[j][3] <= obstacle_list[i][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][1] = min(obstacle_list[i][1], obstacle_list[j][1])
                    del obstacle_list[j]
                    merge = True
                elif obstacle_list[i][1] >= obstacle_list[j][1] and obstacle_list[i][3] <= obstacle_list[j][3]:
                    obstacle_list[i][2] = max(obstacle_list[i][2], obstacle_list[j][2])
                    obstacle_list[i][1] = obstacle_list[j][1]
                    obstacle_list[i][3] = obstacle_list[j][3]
                    del obstacle_list[j]
                    merge = True

            if merge is False:
                j += 1
            else:
                j = i + 1


def obstacle(obstacle_frame):
    play_canny = imf.make_canny(obstacle_frame)
    object_list = []

    _, roi_contours, roi_hierarchy = cv2.findContours(play_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] == -1:
            if rect_area >= 550:
                # object_list.append([x+main.wx1, y+main.wy1, x+w+main.wx1, y+h+main.wy1])
                # object_list.append([x, y, x + w, y + h])
                # object_list.append([x+wx1, y+wy1, x+wx1 + w, y+wy1 + h])
                object_list.append([x + ws.wx1, y + ws.wy1, x + ws.wx1 + w, y + ws.wy1 + h])

    make_obstacle_list(object_list)

    obstacle_list = []
    jelly_list = []
    for i in range(len(object_list)):
        x, y, w, h = object_list[i]
        if y <= ws.wy1 + 10:
            obstacle_list.append(object_list[i])
            # cv2.rectangle(frame, (x, y), (w, h), (0, 0, 255), 2)
        elif h >= ws.wy2 - 15:
            obstacle_list.append(object_list[i])
            # cv2.rectangle(frame, (x, y), (w, h), (0, 0, 255), 2)
        else:
            jelly_list.append(object_list[i])
            # cv2.rectangle(obstacle_frame, (x, y), (w, h), (0, 255, 0), 2)

    return obstacle_list, jelly_list
