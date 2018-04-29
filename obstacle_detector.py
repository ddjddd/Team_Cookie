import cv2


def get_roi_window_size(hgt, wth):
    wx1 = int(wth * 30 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 15 / 100)
    wy2 = int(hgt * 81 / 100)
    return wx1, wx2, wy1, wy2


def lister(list):
    list.sort()
    for i in range(len(list)):
        j = i + 1
        while j < len(list):
            merge = False
            if list[i][2] >= list[j][0]:
                if list[i][1] <= list[j][1] <= list[i][3]:
                    list[i][2] = max(list[i][2], list[j][2])
                    list[i][3] = max(list[i][3], list[j][3])
                    del list[j]
                    merge = True
                elif list[i][1] <= list[j][3] <= list[i][3]:
                    list[i][2] = max(list[i][2], list[j][2])
                    list[i][1] = min(list[i][1], list[j][1])
                    del list[j]
                    merge = True
                elif list[i][1] >= list[j][1] and list[i][3] <= list[j][3]:
                    list[i][2] = max(list[i][2], list[j][2])
                    list[i][1] = list[j][1]
                    list[i][3] = list[j][3]
                    del list[j]
                    merge = True

            if merge is False:
                j += 1
            else:
                j = i + 1


def detector(roi_frame, height, width):
    roi_blur = cv2.GaussianBlur(roi_frame, (3, 3), 0)
    roi_canny = cv2.Canny(roi_blur, 170, 200)
    obstacle_list = []

    _, roi_contours, roi_hierarchy = cv2.findContours(roi_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] is not -1:
            if rect_area >= 550:
                obstacle_list.append([x, y, x+w, y+h])

    lister(obstacle_list)

    for i in range(len(obstacle_list)):
        x, y, w, h = obstacle_list[i]
        if y <= 10:
            cv2.rectangle(roi_frame, (x, y), (w, h), (0, 0, 255), 2)
        elif h >= height - 13:
            cv2.rectangle(roi_frame, (x, y), (w, h), (0, 0, 255), 2)
        else:
            cv2.rectangle(roi_frame, (x, y), (w, h), (0, 255, 0), 2)


    return
