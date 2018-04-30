# import numpy as np
# import cv2
#
#
# # defining the Range of yellow color - 이 값은 HSV trackbar을 실시하면서 얻어냈다
# # yellow : 노란색 곰젤리, 코인
# yellow_lower = np.array([22, 60, 200], np.uint8)
# yellow_upper = np.array([60, 255, 255], np.uint8)
#
# # pink : 분홍색 곰젤리
# pink_lower = np.array([169, 96, 220], np.uint8)
# pink_upper = np.array([174, 140, 255], np.uint8)
#
# # blue : 파란색 기본 젤리
# blue_lower = np.array([85, 103, 133], np.uint8)
# blue_upper = np.array([104, 232, 255], np.uint8)
#
# yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
# pink = cv2.inRange(hsv, pink_lower, pink_upper)
# blue = cv2.inRange(hsv, blue_lower, blue_upper)
#
# yellow = cv2.dilate(yellow, kernel)
# res1 = cv2.bitwise_and(frame, frame, mask=yellow)
#
# pink = cv2.dilate(pink, kernel)
# res2 = cv2.bitwise_and(frame, frame, mask=pink)
#
# blue = cv2.dilate(blue, kernel)
# res3 = cv2.bitwise_and(frame, frame, mask=blue)
#
# # Tracking the yellow Color
# # OpenCV에서 contours를 찾고, 그리기 위해서 아래 2개의 함수를 사용.
# # 1. contours를 찾는 방법: 모든 contours line을 찾으며, 모든 hieracy관계를 구성함.
# # 2. contours line을 그릴 수 있는 point 만 저장. (ex; 사각형이면 4개 point)
# (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for pic, contour in enumerate(contours):
#     # Contour의 면적을 구하는 부분
#     area = cv2.contourArea(contour)
#     if (area > 100):
#         # frame=cv2.drawContours(frame, contour, -1, (0,255,0), 3)
#         x, y, w, h = cv2.boundingRect(contour)
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
#
# # pink
# (_, contours, hierarchy) = cv2.findContours(pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for pic, contour in enumerate(contours):
#     area = cv2.contourArea(contour)
#     if (area > 30):
#         # frame = cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
#         x, y, w, h = cv2.boundingRect(contour)
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# # blue
# (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for pic, contour in enumerate(contours):
#     area = cv2.contourArea(contour)
#     if (area > 100):
#         # frame = cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
#         x, y, w, h = cv2.boundingRect(contour)
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

