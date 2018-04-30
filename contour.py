# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread('img/map5.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 10)    # canny threshold(image, threshold1, threshold2)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cv2.imshow("contours", edged)

width, height, channels = image.shape

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

'''
# ----------- 2018.04.08 -------------- #
mov, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# mov=cv2.drawContours(combine, contours, -1, (0, 255, 0), 2)

for i in range(len(cnts)):    # 모든 외곽선 집합에 대하여 검사
    x, y, w, h = cv2.boundingRect(cnts[i])    # 현재 점수 외곽선의 좌표 받아오기
    rect_area = w * h               # 외곽선의 넓이
    aspect_ratio = float(w) / h     # 외관선의 너비-높이 비율

    # 비율, 넓이의 기준치에 도달하는 외관선들만 선택
    if rect_area >= 1000 and y < int(height * 90/100) and x > int(width*30/100) and x < int(height*80/100):
        # cv2.drawContours(frame, [contours[i]], 0, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255,255,255), 1)

cv2.imshow('image', image)
cv2.waitKey(0)
# -------------------------------------- #
'''

# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None


detected_list_A=[]
detected_list_B=[]
obstacle_dic={}
idx = 0
# loop over the contours individually
for c in cnts:
    idx+=1
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
        idx-=1
        continue

    # compute the rotated bounding box of the contour
    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)


    # loop over the original points and draw them
    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    # unpack the ordered bounding box, then compute the midpoint
    # between the top-left and top-right coordinates, followed by
    # the midpoint between bottom-left and bottom-right coordinates
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)

    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-righ and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    # draw the midpoints on the image
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
             (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
             (255, 0, 255), 2)
    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    detected_list_A.append(dA)  # height
    detected_list_B.append(dB)

    # 위에서 내려오는 장애물(슬라이딩)
    if dA > 300:
        obstacle_dic.update({idx:dA})
    # 땅에서 붙은 장애물(점프)


    print(dA)
    print(dB)
    print('=====')

    # if the pixels per metric has not been initialized, then
    # compute it as the ratio of pixels to supplied metric
    # (in this case, inches)
    if pixelsPerMetric is None:
        pixelsPerMetric = dB / 2

    # compute the size of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    print(dimA)
    print(dimB)
    print('-----------------')
    # draw the object sizes on the image
    cv2.putText(orig, "{:.1f}".format(dA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}".format(dB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
    # show the output image
    cv2.imshow("Image", orig)
    cv2.waitKey()

print('------- detected list A ---------')
for i in detected_list_A:
    print(i)

print('------- detected list B ---------')
for i in detected_list_B:
    print(i)

print('--------- estimated obstacle(height>300) ----------')
for key, val in obstacle_dic.items():
    print(key, val)