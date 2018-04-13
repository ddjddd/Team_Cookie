import cv2


def get_roi_window_size(height, width):
    wx1 = int(width * 30 / 100)
    wx2 = int(width * 80 / 100)
    wy1 = int(height * 15 / 100)
    wy2 = int(height * 80 / 100)
    return wx1, wx2, wy1, wy2


def detector(roi_frame, height, width):
    roi_blur = cv2.GaussianBlur(roi_frame, (3, 3), 0)
    roi_canny = cv2.Canny(roi_blur, 150, 200)
    rx = 10000

    wx1, wx2, wy1, wy2 = get_roi_window_size(height, width)
    # cv2.line(roi_frame, (0, 300), (width, 300), (0, 0, 255), 3)
    _, roi_contours, _ = cv2.findContours(roi_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in range(len(roi_contours)):
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        aspect_ratio = float(w) / h
        if rect_area >= 500:
            # print(y + h)
            # cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

            # cv2.rectangle(roi_frame, (x+w-1, y+h-1), (x + w, y + h), (255, 255, 255), 2)

            if abs(rx - x) > 5:
                if y+h >= 295 and aspect_ratio <= 0.95:
                    cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    rx = x
    return
