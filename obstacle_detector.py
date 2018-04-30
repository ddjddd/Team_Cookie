import cv2


def get_roi_window_size(hgt, wth):
    wx1 = int(wth * 30 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 15 / 100)
    wy2 = int(hgt * 81 / 100)
    return wx1, wx2, wy1, wy2


def detector(roi_frame, height, width):
    roi_blur = cv2.GaussianBlur(roi_frame, (3, 3), 0)     # 입력 이미지 블러처리
    roi_canny = cv2.Canny(roi_blur, 170, 200)    # 블러된 이미지에 대한 canny edge coutour
    rx = 10000

    ob_threshhold = int(height * 93 / 100)

    # 바닥 좌표를 기준으로 흰색 선을 표시
    cv2.line(roi_frame, (0, ob_threshhold), (width, ob_threshhold), (255, 255, 255), 3)

    # findCountours()은 image, contours , hierachy를 리턴한다
    _, roi_contours, roi_hierarchy = cv2.findContours(roi_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(roi_contours)):
        # 컨투어를 기준으로 생기는 사각형boundingRect의 좌표xy, 크기wh
        x, y, w, h = cv2.boundingRect(roi_contours[i])
        rect_area = w * h
        aspect_ratio = float(w) / h

        # roi_hierarchy: 4칸짜리 배열, 각 컨투어 간의 관계를 나타내줌. 3번째 요소가 -1이면 제일 바깥쪽에 있는 컨투어
        if roi_hierarchy[0][i][3] is not -1:
            # cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if rect_area >= 550:   # 감지된 물체의 기준 크기
                if y+h >= ob_threshhold :  # 바닥 기준 이상 = 장애물
                    cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)    # 장애물에 사각형

    cv2.imshow('obs', roi_canny)   # 컨투어 화면
    cv2.imshow('Obstacles', roi_frame)    # 바닥선 기준으로 크롭된 화면
    # cv2.destroyAllWindows()
    return
