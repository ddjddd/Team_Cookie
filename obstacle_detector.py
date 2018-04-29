import cv2


def get_roi_window_size(hgt, wth):
    wx1 = int(wth * 30 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 15 / 100)
    wy2 = int(hgt * 81 / 100)
    return wx1, wx2, wy1, wy2


def detector(roi_frame, height, width):
    roi_blur = cv2.GaussianBlur(roi_frame, (3, 3), 0)
    roi_canny = cv2.Canny(roi_blur, 170, 200)
    rx = 10000

    ob_threshhold = int(height * 93 / 100)

    cv2.line(roi_frame, (0, ob_threshhold), (width, ob_threshhold), (255, 255, 255), 3)
    _, roi_contours, roi_hierarchy = cv2.findContours(roi_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        aspect_ratio = float(w) / h
        if roi_hierarchy[0][i][3] is not -1:
            # cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if rect_area >= 550:
                if y+h >= ob_threshhold :
                    cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('obs', roi_canny)
    cv2.imshow('Obstacles', roi_frame)
    # cv2.destroyAllWindows()
    return
