# importing modules

import cv2
import numpy as np

# capturing video through webcam
cap = cv2.VideoCapture("cookierun.mp4")

# defining the Range of yellow color - 이 값은 HSV trackbar을 실시하면서 얻어냈다
# yellow : 노란색 곰젤리, 코인
yellow_lower = np.array([22, 60, 200], np.uint8)
yellow_upper = np.array([60, 255, 255], np.uint8)

# pink : 분홍색 곰젤리
pink_lower = np.array([169, 96, 220], np.uint8)
pink_upper = np.array([174, 140, 255], np.uint8)

# blue : 파란색 기본 젤리
blue_lower = np.array([85, 103, 133], np.uint8)
blue_upper = np.array([104, 232, 255], np.uint8)

# brown : 쿠키(투명해지는 범위까지 최대한 포함시키고자 했으나 투명해지는 부분에서 detection은 X)
brown_lower = np.array([10, 112, 210], np.uint8)
brown_upper = np.array([15, 180, 255], np.uint8)


## transp - 투명해진 쿠키만 따로 범위를 뽑아냄
transp_lower = np.array([2, 108, 143], np.uint8)
transp_upper = np.array([16, 203, 201], np.uint8)

# transp2 검은색 배경의 투명해진 쿠키.... ( 배경이 달라지면 trans3가 필요할 수 도 있음... )
transp2_lower = np.array([7, 73, 94, ], np.uint8)
transp2_upper = np.array([21, 189, 184, ], np.uint8)

# 그리드의 한 칸에 타겟이 있는지 여부
# unit = 그리드 한 칸(정사각형)의 길이,
# x,y =  확인할 그리드 한 칸의 왼쪽 모서리 좌표
# target_x ~ target_h = 인식할 타겟의 좌표 밑 높이, 너비
def in_grid(unit, x, y, target_x, target_y, target_w, target_h):
    #그리드와 타켓의 좌표 범위
    x_range=set( range(x,x+unit+1) )
    y_range=set(range(y,y+unit +1))
    target_x_range = list(range(target_x, target_x + target_w))
    target_y_range = list(range(target_y, target_y + target_h))
    # 그리드 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersectx = [value for value in target_x_range if value in x_range]
    intersecty = [value for value in target_y_range if value in y_range]

    if len(intersectx) > unit/2  and  len(intersecty) >= unit/2:
        return True
    else:
        return False


ret, frame = cap.read()
kernel = np.ones((5, 5), "uint8")
cordinate_get = False
window_y, window_x, _ = frame.shape # 화면의 크기
print(window_x)
print(window_y)
while (ret):
    grid = frame.copy() # gird 용 이미지

    # frame을 HSV (hue-saturation-value)로 변환한다
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 해당 범위에 속하는 각 색깔을 찾는다
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    pink = cv2.inRange(hsv, pink_lower, pink_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    brown = cv2.inRange(hsv, brown_lower, brown_upper)
    transp = cv2.inRange(hsv, transp_lower, transp_upper)
    transp2 = cv2.inRange(hsv, transp2_lower, transp2_upper)
    go = 1
    cookie_detected = False

    #dilate: morphology 연산 중 하나. 구조 요소를 사용하여 이웃한 화소들 중 최대 화소값으로 대체한다.
    # 즉, 어두운 영역이 줄어들며 밝은 영역이 늘어남. 노이즈 제거 후 줄어든 크기를 복구하고자 할 때 주로 사용.
    # bitwise_and 연산자는 둘다 0이 아닌 경우만 값을 통과 시킴.
    # 원본 이미지와 마스크 이미지를 AND 연산하여 노란색만 추출한다. 즉 mask 영역 이외는 모두 제거됨.
    yellow = cv2.dilate(yellow, kernel)
    res1 = cv2.bitwise_and(frame, frame, mask=yellow)

    pink = cv2.dilate(pink, kernel)
    res2 = cv2.bitwise_and(frame, frame, mask=pink)

    blue = cv2.dilate(blue, kernel)
    res3 = cv2.bitwise_and(frame, frame, mask=blue)

    brown = cv2.dilate(brown, kernel)
    res4 = cv2.bitwise_and(frame, frame, mask=brown)

    transp = cv2.dilate(transp, kernel)
    res5 = cv2.bitwise_and(frame, frame, mask=transp)

    transp2 = cv2.dilate(transp2, kernel)
    res6 = cv2.bitwise_and(frame, frame, mask=transp2)

    # Tracking the yellow Color
    # OpenCV에서 contours를 찾고, 그리기 위해서 아래 2개의 함수를 사용.
    # 1. contours를 찾는 방법: 모든 contours line을 찾으며, 모든 hieracy관계를 구성함.
    # 2. contours line을 그릴 수 있는 point 만 저장. (ex; 사각형이면 4개 point)
    (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        # Contour의 면적을 구하는 부분
        area = cv2.contourArea(contour)
        if (area > 100):

            #frame=cv2.drawContours(frame, contour, -1, (0,255,0), 3)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    #pink
    (_, contours, hierarchy) = cv2.findContours(pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 30):
            #frame = cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #blue
    (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 100):
            #frame = cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cookie

    (_, contours, hierarchy) = cv2.findContours(brown, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 밤 때문에 가려지는 경우가 존재.
    for pic, contour in enumerate(contours):

        area = cv2.contourArea(contour)
        hierarchy_num = hierarchy[0][pic][-1]
        x, y, w, h = cv2.boundingRect(contour)
        if  y<400 and 2000 < area and (200 < x +w/2) and (x+w/2 < 240) and hierarchy_num == -1:

            cookie_detected = True # 투명한 쿠키를 디텍션할 필요 없음
            cookie_save_x ,cookie_save_y, cookie_save_w, cookie_save_h = x, y, w, h # 인식한 쿠키 좌표 저장
            #res4 = cv2.rectangle(res4, (x, y), (x + w, y + h), (170, 100, 69), 2)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (170, 100, 69), 2)

    #transp cookie
    if not cookie_detected:
        (_, contours, hierarchy) = cv2.findContours(transp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #hierarchy_num = hierarchy[0][pic][-1]

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if  y<400 and 2000 < area and (200 < x +w/2) and (x+w/2 < 240) :#and hierarchy_num == -1:
                cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h = x, y, w, h
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cookie_detected = True

    #trnsp cookie 2
    if not  cookie_detected:
        (_, contours, hierarchy) = cv2.findContours(transp2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if y < 390 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240) and w<100:  # and hierarchy_num == -1:
                cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h = x, y, w ,h
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                res6 = cv2.rectangle(res6, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cookie_detected = True
                #cv2.imshow("cookie trans mask", res6)
                #go = 0


    #쿠키를 찾지 못하였을 때 전 프래임의 쿠키 위치를 그대로 사용
    if not cookie_detected:
        x, y, w, h = cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)


    #draw gird
    if not cordinate_get:
        grid_unit_length  = int(cookie_save_w/2) # 처음 발견한 쿠키의 너비의 절반을 그리드 단위길이로

        # 쿠키의 중심을 찾음
        cookie_center_x, cookie_center_y = int(cookie_save_x + cookie_save_w / 2), int(
            cookie_save_y + cookie_save_h / 2)

        # 그리드의 위치는 쿠키의 위치를 활용해 설정
        grid_x_start = cookie_center_x + grid_unit_length * -2
        grid_y_start = cookie_save_y + cookie_save_h + grid_unit_length * -8

        cordinate_get = True


    # 가로 12칸, 세로 9칸
    verticle_num = 12
    horizontal_num = 9

    # 그리드 가로 선
    for verticle in range(verticle_num+1):
        grid_x = cookie_center_x +  grid_unit_length * verticle
        cv2.line(grid,
                (grid_x_start + grid_unit_length * verticle, grid_y_start),
                (grid_x_start+ grid_unit_length* verticle, grid_y_start  + grid_unit_length * horizontal_num),
                 (0, 0, 0), 2, 1)
    # 그리드 세로 선
    for horizontal in range(horizontal_num +1):
        cv2.line(grid,
                 (grid_x_start, grid_y_start  + grid_unit_length * horizontal),
                 (grid_x_start + grid_unit_length * verticle_num,  grid_y_start  + grid_unit_length * horizontal),
                 (0,0,0),2,1)

    # 그리드 한 칸마다 쿠키(혹은 다른 물체) 가 있는지 확인하기
    for ver in range(verticle_num):
        for hor in range(horizontal_num):
            if in_grid(grid_unit_length, grid_x_start+ver*grid_unit_length, grid_y_start+hor*grid_unit_length, cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h) :
                #쿠키가 있다고 판단된 그리드 좌표
                x_to_color = grid_x_start + ver * grid_unit_length
                y_to_color = grid_y_start + hor * grid_unit_length
                #회색으로 칠함
                grid[ y_to_color: y_to_color + grid_unit_length, x_to_color: x_to_color+grid_unit_length ] = (100,100,100)

    cv2.imshow("Color Tracking", frame)
    cv2.imshow('grid', grid)
    if cv2.waitKey(go) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()


cap.release()
cv2.destroyAllWindows()

