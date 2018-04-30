from src import grid
from src.detectors import cookie as ck


def in_grid(x, y, target_x, target_y, target_w, target_h):
    global unit
    # 그리드와 타켓의 좌표 범위
    x_range = set(range(x, x + unit + 1))
    y_range = set(range(y, y + unit + 1))
    target_x_range = list(range(target_x, target_x + target_w))
    target_y_range = list(range(target_y, target_y + target_h))
    # 그리드 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in target_x_range if value in x_range]
    intersect_y = [value for value in target_y_range if value in y_range]

    if len(intersect_x) >= unit/2 and len(intersect_y) >= unit/2:
        return True
    else:
        return False


def cookie_collision(cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h):
    # 그리드 한 칸마다 쿠키(혹은 다른 물체) 가 있는지 확인하기
    for ver in range(grid.vertical_num):
        for hor in range(grid.horizontal_num):
            if grid.in_grid(grid.grid_x + ver * grid.unit, grid.grid_y + hor * grid.unit,
                            cookie_save_x, cookie_save_y, cookie_save_w, cookie_save_h):
                # 쿠키가 있다고 판단된 그리드 좌표
                x_to_color = grid.grid_x + ver * grid.unit
                y_to_color = grid.grid_y + hor * grid.unit
                # 회색으로 칠함
                frame[y_to_color: y_to_color + grid.unit, x_to_color: x_to_color + grid.unit] = (100, 100, 100)
