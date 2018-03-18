from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
import numpy as np

x1, y1, x2, y2 = 210, 307, 230, 325
frame = None
frame2 = None
rectangle = False
trackWindow  = None

# 화면 전체 마스크용 함수
def only_cookie(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cookie_min = np.array([170, 100, 60])
    cookie_max = np.array([255, 180, 120])

    mask = cv2.inRange(image, cookie_min, cookie_max)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 작은 구멍들 메꿈
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 노이즈 제거

    image = cv2.bitwise_and(image, image, mask=mask)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # #gray = cv2.equalizeHist(gray)
    return image

# 트랙 윈도우 초기화 함수
def initialize():
    global roi_hist
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    height, width = abs(y1 - y2), abs(x1 - x2)
    trackWindow = (x1, y1, width, height)
    roi = frame[y1:y1 + height, x1:x1 + width]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180])

    return trackWindow

# camShift 구현용 메인함수
def camShift():
    global frame, frame2, trackWindow, roi_hist, out

    cap = cv2.VideoCapture('cookierun.mp4')
    ret, frame = cap.read()
    frame = only_cookie(frame)
    cv2.namedWindow('frame')
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    # 트래킹 관심 영역 초기값 설정
    trackWindow = initialize()

    while True:
        # 동영상 입력 받기
        ret, frame = cap.read()
        original = frame
        frame = only_cookie(frame)

        if not ret:
            break

        if trackWindow is not None:
            # 추적 실패 예외처리
            if trackWindow[1] > 390 :                   # y값 튀는 경우
                temp = list(trackWindow)
                temp[1] = temp[1] - 200
                trackWindow = tuple(temp)
            if trackWindow[0] < 5 :                     # x값 바닥보다 밑인경우
                temp = list(trackWindow)
                temp[1] = temp[0] + 5
                trackWindow = tuple(temp)
            if trackWindow[2] - trackWindow[0] > 300 :  # 트랙윈도우 너비 커질때
                trackWindow = initialize()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            ret, trackWindow = cv2.CamShift(dst, trackWindow, termination)

            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            cv2.polylines(original, [pts], True, (0, 255, 0), 2)

        cv2.imshow('frame', frame)      # 마스크 이미지
        cv2.imshow('frame2', original)  # 원본 이미지

        k = 0xFF
        if k == 27:         # 종료
            break;
        if k == ord('i'):   #일시정지
            cv2.waitKey(0)

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


camShift()
