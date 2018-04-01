# importing modules
import cv2
import numpy as np

# capturing video through webcam
cap = cv2.VideoCapture("cookierun.mp4")


while (1):
    ret, frame = cap.read()

    # frame을 HSV (hue-saturation-value)로 변환한다
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # defining the Range of yellow color - 이 값은 HSV trackbar을 실시하면서 얻어냈다
    #yellow : 노란색 곰젤리, 코인
    # yellow_lower = np.array([22, 60, 200], np.uint8)
    # yellow_upper = np.array([60, 255, 255], np.uint8)
    #
    # #pink : 분홍색 곰젤리
    # pink_lower = np.array([169, 96, 220], np.uint8)
    # pink_upper = np.array([174, 140, 255], np.uint8)
    #
    # #blue : 파란색 기본 젤리
    # blue_lower = np.array([85, 103, 133], np.uint8)
    # blue_upper = np.array([104, 232, 255], np.uint8)
    #
    # #brown : 쿠키(투명해지는 범위까지 최대한 포함시키고자 했으나 투명해지는 부분에서 detection은 X)
    brown_lower = np.array([12, 136, 201], np.uint8)
    brown_upper = np.array([15, 173, 232], np.uint8)

    # # 해당 범위에 속하는 각 색깔을 찾는다
    # yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    # pink = cv2.inRange(hsv, pink_lower, pink_upper)
    # blue = cv2.inRange(hsv, blue_lower, blue_upper)
    brown = cv2.inRange(hsv, brown_lower, brown_upper)
    print(brown)


    # Morphological transformation, Dilation
    kernel = np.ones((5, 5), "uint8")

    #dilate: morphology 연산 중 하나. 구조 요소를 사용하여 이웃한 화소들 중 최대 화소값으로 대체한다.
    # 즉, 어두운 영역이 줄어들며 밝은 영역이 늘어남. 노이즈 제거 후 줄어든 크기를 복구하고자 할 때 주로 사용.
    #yellow = cv2.dilate(yellow, kernel)
    # bitwise_and 연산자는 둘다 0이 아닌 경우만 값을 통과 시킴.
    # 원본 이미지와 마스크 이미지를 AND 연산하여 노란색만 추출한다. 즉 mask 영역 이외는 모두 제거됨.
    #res1 = cv2.bitwise_and(frame, frame, mask=yellow)

    # pink = cv2.dilate(pink, kernel)
    # res2 = cv2.bitwise_and(frame, frame, mask=pink)
    #
    # blue = cv2.dilate(blue, kernel)
    # res3 = cv2.bitwise_and(frame, frame, mask=blue)

    brown = cv2.dilate(brown, kernel)
    res4 = cv2.bitwise_and(frame, frame, mask=brown)

    # Tracking the yellow Color
    # OpenCV에서 contours를 찾고, 그리기 위해서 아래 2개의 함수를 사용.
    # 1. contours를 찾는 방법: 모든 contours line을 찾으며, 모든 hieracy관계를 구성함.
    # 2. contours line을 그릴 수 있는 point 만 저장. (ex; 사각형이면 4개 point)
    # (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     # Contour의 면적을 구하는 부분
    #     area = cv2.contourArea(contour)
    #     if (area > 100):
    #         #frame=cv2.drawContours(frame, contour, -1, (0,255,0), 3)
    #         x, y, w, h = cv2.boundingRect(contour)
    #         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #
    #
    # #pink
    # (_, contours, hierarchy) = cv2.findContours(pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 30):
    #         #frame = cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
    #         x, y, w, h = cv2.boundingRect(contour)
    #         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #
    # #blue
    # (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 100):
    #         #frame = cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
    #         x, y, w, h = cv2.boundingRect(contour)
    #         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #brown
    (_, contours, hierarchy) = cv2.findContours(brown, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 500):
            # frame = cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (170, 100, 69), 2)


    cv2.imshow("Color Tracking", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

