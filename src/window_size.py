# 각각의 윈도우 사이즈를 반환하는 모듈


# 게임 플레이 주요 화면
def get_play_window_size(hgt, wth):
    wx1 = int(wth * 30 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 15 / 100)
    wy2 = int(hgt * 81 / 100)
    return wx1, wx2, wy1, wy2


# 바닥 화면
def get_ground_size(hgt, wth):
    wx1 = int(wth * 20 / 100)
    wx2 = int(wth * 80 / 100)
    wy1 = int(hgt * 80 / 100)
    wy2 = int(hgt * 90 / 100)
    return wx1, wx2, wy1, wy2


# 체력 표시 부분의 사이즈 설정
def get_health_size(hgt, wth):
    hx1 = int(wth * 7 / 100)
    hx2 = int(wth * 90 / 100)
    hy1 = int(hgt * 10 / 100)
    hy2 = int(hgt * 15 / 100)
    return hx1, hx2, hy1, hy2


# 점수 표시 부분의 사이즈 설정
def get_score_size(hgt, wth):
    sx1 = int(wth * 60 / 100)
    sx2 = int(wth * 95 / 100)
    sy1 = int(hgt * 1 / 100)
    sy2 = int(hgt * 7 / 100)
    return sx1, sx2, sy1, sy2
