################################
################################
# 모듈명    : grid
# 작성자    : 이석범
# 설명      : 화면에 그리드를 출력
################################
################################

import cv2
from src.detectors import cookie as ck

# 전역 변수 선언 및 초기화
unit = 0                               # 그리드 한 칸(정사각형)의 길이
vertical_max, horizontal_max = 12, 9   # 가로 12칸, 세로 9칸
grid_x, grid_y = 0, 0                  # 그리드의 시작지점. 변수 초기화


################################
# 함수명    : draw_grid
# 작성자    : 이석범
# 설명      : 입력된 화면에 그리드 출력 ( 격자 형태 )
# 리턴      : _
# 매개변수  : image frame 전체 화면
################################
def draw_grid(frame):
    global unit

    # 그리드 가로선 그리기
    for ver in range(vertical_max + 1):
        cv2.line(frame,
                 (grid_x + unit * ver, grid_y),
                 (grid_x + unit * ver, grid_y + unit * horizontal_max),
                 (40, 40, 40), 2, 1)

    # 그리드 세로선 그리기
    for hor in range(horizontal_max + 1):
        cv2.line(frame,
                 (grid_x, grid_y + unit * hor),
                 (grid_x + unit * vertical_max, grid_y + unit * hor),
                 (40, 40, 40), 2, 1)


################################
# 함수명    : set_grid
# 작성자    : 이석범
# 설명      : 최초 1회만 동작
#             입력된 화면에서 쿠키의 위치를 찾고 이를 기준으로 그리드 생성에 필요한 변수를 설
# 리턴      : Boolean
# 매개변수  : image frame 쿠키를 검출할 화면
################################
def set_grid(frame):
    global unit, grid_x, grid_y

    # frame을 HSV (hue-saturation-value)로 변환한다
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 해당 범위에 속하는 각 색깔을 찾는다
    brown = cv2.inRange(hsv, ck.brown_lower, ck.brown_upper)
    brown = cv2.dilate(brown, ck.kernel)

    # 쿠키 윤곽선 검출        # 밤 때문에 가려지는 경우가 존재.
    _, contours, hierarchy = cv2.findContours(brown, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        hierarchy_num = hierarchy[0][pic][-1]
        x, y, w, h = cv2.boundingRect(contour)

        if y < 400 and 2000 < area and (200 < x + w / 2) and (x + w / 2 < 240) and hierarchy_num == -1:
            initial_x, initial_y, initial_w, initial_h = x, y, w, h     # 인식한 쿠키 좌표 저장
            break;
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (170, 100, 69), 2)

    try:
        unit = int(initial_w / 2)   # 처음 발견한 쿠키의 너비의 절반을 그리드 단위길이로
        grid_x = initial_x - unit
        grid_y = initial_y + initial_h + unit * -8
        # print('grid true')
        return True
    except:
        return False

















