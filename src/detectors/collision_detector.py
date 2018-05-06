from src import grid
from src import main
from src import window_size as ws


def in_grid(x, y, target_x, target_y, target_w, target_h):
    # 그리드와 타켓의 좌표 범위
    x_range = set(range(x, x + grid.unit + 1))
    y_range = set(range(y, y + grid.unit + 1))
    target_x_range = list(range(target_x, target_w))
    target_y_range = list(range(target_y, target_h))
    # 그리드 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in target_x_range if value in x_range]
    intersect_y = [value for value in target_y_range if value in y_range]

    if len(intersect_x) >= grid.unit/3 and len(intersect_y) >= grid.unit/3:
        return True
    else:
        return False


def in_grid_ground(x, y, target_x, target_y, target_w, target_h):
    # 그리드와 타켓의 좌표 범위
    x_range = set(range(x, x + grid.unit + 1))
    y_range = set(range(y, y + grid.unit + 1))
    target_x_range = list(range(target_x, target_w))
    target_y_range = list(range(target_y, target_h))
    # 그리드 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in target_x_range if value in x_range]
    intersect_y = [value for value in target_y_range if value in y_range]

    if len(intersect_x) >= grid.unit/5 and len(intersect_y) >= grid.unit/5:
        return True
    else:
        return False


def cookie_collision(matrix, frame, save_x, save_y, save_w, save_h):
    # 그리드 한 칸마다 쿠키(혹은 다른 물체) 가 있는지 확인하기
    for ver in range(grid.vertical_max):
        for hor in range(grid.horizontal_max):
            if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit, save_x, save_y, save_x + save_w, save_y + save_h):
                # 쿠키가 있다고 판단된 그리드 좌표
                color_x = grid.grid_x + ver * grid.unit
                color_y = grid.grid_y + hor * grid.unit
                # 회색으로 칠함
                frame[color_y: color_y + grid.unit, color_x: color_x + grid.unit] = (170, 100, 69)
                matrix[hor][ver] = '$'


def obstacle_collision(matrix, obstacle_list):
    for i in range(len(obstacle_list)):
        for ver in range(grid.vertical_max):
            for hor in range(grid.horizontal_max):
                if in_grid_ground(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,

                                  obstacle_list[i][0], obstacle_list[i][1], obstacle_list[i][2], obstacle_list[i][3]):
                    matrix[hor][ver] = '#'



def jelly_collision(matrix, jelly_list):
    for i in range(len(jelly_list)):
        for ver in range(grid.vertical_max):
            for hor in range(grid.horizontal_max):
                if in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                                  jelly_list[i][0], jelly_list[i][1], jelly_list[i][2], jelly_list[i][3]):
                    matrix[hor][ver] = '%'


def ground_collision(matrix, ground_list):
    for i in range(len(ground_list)):
        for ver in range(grid.vertical_max):
            for hor in range(grid.horizontal_max):
                if in_grid_ground(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                                  ground_list[i][0], ground_list[i][1], ground_list[i][2], ground_list[i][3]):
                    matrix[hor][ver] = '&'

# def ground_collision(frame, ground_list):
#     for i in range(len(ground_list)):
#         for ver in range(grid.vertical_max):
#             for hor in range(grid.horizontal_max):
#                 # print(ground_list[i][0], ground_list[i][1], ground_list[i][2], ground_list[i][3])
#                 if in_grid_ground(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
#                                   ground_list[i][0], ground_list[i][1], ground_list[i][2], ground_list[i][3]):
#                     # 쿠키가 있다고 판단된 그리드 좌표
#                     color_x = grid.grid_x + ver * grid.unit
#                     color_y = grid.grid_y + hor * grid.unit
#                     # 회색으로 칠함
#                     frame[color_y: color_y + grid.unit, color_x: color_x + grid.unit] = (100, 69, 170)

# def obstacle_collision(frame, obstacle_list):
#     for i in range(len(obstacle_list)):
#         for ver in range(grid.vertical_max):
#             for hor in range(grid.horizontal_max):
#                 # print(ground_list[i][0], ground_list[i][1], ground_list[i][2], ground_list[i][3])
#                 if in_grid_ground(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
#                                   obstacle_list[i][0], obstacle_list[i][1], obstacle_list[i][2], obstacle_list[i][3]):
#                     # 쿠키가 있다고 판단된 그리드 좌표
#                     color_x = grid.grid_x + ver * grid.unit
#                     color_y = grid.grid_y + hor * grid.unit
#                     # 회색으로 칠함
#                     frame[color_y: color_y + grid.unit, color_x: color_x + grid.unit] = (69, 170, 100)


