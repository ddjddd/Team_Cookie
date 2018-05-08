################################
################################
# 모듈명    : window_size
# 작성자    : 최진호
# 설명      : 화면 분할용 모듈
################################
################################

# 전역변수 선언 및 초기화
wx1, wx2, wy1, wy2 = 0, 0, 0, 0
gx1, gx2, gy1, gy2 = 0, 0, 0, 0
cx1, cx2, cy1, cy2 = 0, 0, 0, 0


################################
# 함수명    : get_cookie_size
# 작성자    : 최진호
# 설명      : 쿠키 화면 분할
# 리턴      : int 쿠키 화면 좌표 (x1, x2, y1, y2)
# 매개변수  : int hgt 전체 프레임의 높이
#             int wth 전체 프레임의 너비
################################
def get_cookie_size(hgt, wth):
    global cx1, cx2, cy1, cy2

    cx1 = int(wth * 15 / 100)
    cx2 = int(wth * 35 / 100)
    cy1 = 0
    cy2 = int(hgt * 90 / 100)
    return cx1, cx2, cy1, cy2


################################
# 함수명    : get_play_size
# 작성자    : 최진호
# 설명      : 게임 플레이 화면 분할
# 리턴      : int 게임 플레이 화면 좌표 (x1, x2, y1, y2)
# 매개변수  : int hgt 전체 프레임의 높이
#             int wth 전체 프레임의 너비
################################
def get_play_size(hgt, wth):
    global wx1, wx2, wy1, wy2

    wx1 = int(wth * 30 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 15 / 100)
    wy2 = int(hgt * 81 / 100)
    return wx1, wx2, wy1, wy2


################################
# 함수명    : get_ground_size
# 작성자    : 최재필
# 설명      : 뱌닥 화면 분할
# 리턴      : int 바닥 화면 좌표 (x1, x2, y1, y2)
# 매개변수  : int hgt 전체 프레임의 높이
#             int wth 전체 프레임의 너비
################################
def get_ground_size(hgt, wth):
    global gx1, gx2, gy1, gy2

    gx1 = int(wth * 15 / 100)
    gx2 = int(wth * 80 / 100)
    gy1 = int(hgt * 80 / 100)
    gy2 = int(hgt * 90 / 100)
    return gx1, gx2, gy1, gy2


################################
# 함수명    : get_health_size
# 작성자    : 최진호
# 설명      : 체력 화면 분할
# 리턴      : int 체력 화면 좌표 (x1, x2, y1, y2)
# 매개변수  : int hgt 전체 프레임의 높이
#             int wth 전체 프레임의 너비
################################
def get_health_size(hgt, wth):
    hx1 = int(wth * 7 / 100)
    hx2 = int(wth * 90 / 100)
    hy1 = int(hgt * 10 / 100)
    hy2 = int(hgt * 15 / 100)
    return hx1, hx2, hy1, hy2


################################
# 함수명    : get_score_size
# 작성자    : 최진호
# 설명      : 점수 화면 분할
# 리턴      : int 점수 화면 좌표 (x1, x2, y1, y2)
# 매개변수  : int hgt 전체 프레임의 높이
#             int wth 전체 프레임의 너비
################################
def get_score_size(hgt, wth):
    sx1 = int(wth * 60 / 100)
    sx2 = int(wth * 95 / 100)
    sy1 = int(hgt * 1 / 100)
    sy2 = int(hgt * 7 / 100)
    return sx1, sx2, sy1, sy2
