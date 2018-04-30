import cv2
from src import image_filter as imf


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


def obstacle(play_frame, height, width):
    roi_canny = imf.make_canny(play_frame)
    obstacle_list = []

    _, roi_contours, roi_hierarchy = cv2.findContours(roi_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] is not -1:
            if rect_area >= 550:
                obstacle_list.append([x, y, x+w, y+h])

    make_obstacle_list(obstacle_list)

    for i in range(len(obstacle_list)):
        x, y, w, h = obstacle_list[i]
        if y <= 10:
            cv2.rectangle(play_frame, (x, y), (w, h), (0, 0, 255), 2)
        elif h >= height - 10:
            cv2.rectangle(play_frame, (x, y), (w, h), (0, 0, 255), 2)
        else:
            cv2.rectangle(play_frame, (x, y), (w, h), (0, 255, 0), 2)

    return
