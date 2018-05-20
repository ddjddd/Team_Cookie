################################
################################
# 모듈명    : collision_detector
# 작성자    : 이석범, 최진호
# 설명      : 각종 검출된 개체 리스트들과 그리드의 충돌 검사
#             그리드 내에 있다고 판단한 경우 current state matrix 변경
################################
################################

from src import grid
from src import main
from src import window_size as ws
import cv2


################################
# 함수명    : in_grid
# 작성자    : 이석범
# 설명      : 입력된 그리드 안에 개체가 존재하는 경우
#             존재의 판단 기준
#             그리드 총 면적의 1/16 차지
# 리턴      : int x, y 검사할 그리드의 시작좌표
#             int obj_x, obj_y 검사할 개체의 시작 좌표
#             int obj_w, obj_h 검사할 개체의 너비, 높이
# 매개변수  : boolean 입력된 그리드 안에 개체가 존재하는 경우
################################
def in_grid(x, y, obj_x, obj_y, obj_w, obj_h):
    # 검사할 그리드의 좌표 범위
    x_range = set(range(x, x + grid.unit + 1))
    y_range = set(range(y, y + grid.unit + 1))
    # 검사할 개체의 좌표 범위
    obj_x_range = list(range(obj_x, obj_w))
    obj_y_range = list(range(obj_y, obj_h))
    # 그리드 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in obj_x_range if value in x_range]
    intersect_y = [value for value in obj_y_range if value in y_range]

    if len(intersect_x) >= grid.unit/4 and len(intersect_y) >= grid.unit/4:
        return True
    else:
        return False


################################
# 함수명    : cookie_collision
# 작성자    : 이석범
# 설명      : 쿠키가 차지하는 그리드 검출
# 리턴      : _
# 매개변수  : table matrix 현재 화면 그리드, current state matrix
#             int save_x, save_y 쿠키 시작 위치
#             int save_w, save_h 쿠키 너비, 높이
################################
def cookie_collision(matrix, save_x, save_y, save_w, save_h):
    # 그리드 한 칸마다 쿠키가 있는지 확인하기
    for ver in range(grid.vertical_max):
        for hor in range(grid.horizontal_max):
            if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit, save_x, save_y, save_x + save_w, save_y + save_h):
                # 쿠키가 있다고 판단된 그리드 좌표
                color_x = grid.grid_x + ver * grid.unit
                color_y = grid.grid_y + hor * grid.unit
                # 회색으로 칠함
                #cv2.imshow('m',frame)
                frame[color_y: color_y + grid.unit, color_x: color_x + grid.unit] = (170, 100, 69)
                matrix[hor][ver] = 1


################################
# 함수명    : object_collision_detector
# 작성자    : 최진호
# 설명      : 장애물이 차지하는 그리드 검출
# 리턴      : _
# 매개변수  : table matrix 현재 화면 그리드, current state matrix
#             list obstacle_list 검출된 장애물 개체 리스트
#             list jelly_list 검출된 젤리 개체 리스트
#             list ground_list 검출된 바닥 개체 리스트
################################
def object_collision_detector(matrix, obstacle_list, jelly_list, ground_list):
    for ver in range(grid.vertical_max):
        for hor in range(grid.horizontal_max):
            for i in range(len(obstacle_list)):
                if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                           obstacle_list[i][0], obstacle_list[i][1], obstacle_list[i][2], obstacle_list[i][3]):
                    matrix[hor][ver] = 4
            for i in range(len(jelly_list)):
                if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                           jelly_list[i][0], jelly_list[i][1], jelly_list[i][2], jelly_list[i][3]):
                    matrix[hor][ver] = 7
            for i in range(len(ground_list)):
                if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                           ground_list[i][0], ground_list[i][1], ground_list[i][2], ground_list[i][3]):
                    matrix[hor][ver] = 3

