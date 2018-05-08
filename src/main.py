import cv2
import numpy as np
import time
from PIL import ImageGrab
from src import window_size as ws, grid
from src.detectors import obstacles_and_jelly as ob, score as sc, ground as gd, health as ht, cookie as ck
from src.detectors import collision_detector as cd, is_level_up as ilu

monitor = ImageGrab.grab()
monitor = np.array(monitor)[:, :, ::-1].copy()
monitor = monitor.shape[0]
monitor = int(monitor/40)


################################
# 함수명    : screenshots
# 작성자    : 이석범
# 설명      : 현재 에뮬레이터에서 화면을 스크린샷(캡처)
# 리턴      : image 캡처된 화면
# 매개변수  :  _
################################
def screenshots():
    box = (0, monitor, 852, 480+monitor)
    im = ImageGrab.grab(box)    # .convert('RGB')
    frame = np.array(im)[:, :, ::-1].copy()
    return frame


################################
# 함수명    : main
# 작성자    : _
# 설명      : _
# 리턴      : _
# 매개변수  : _
################################
def main():
    ################################
    # 분석할 이미지   : 동영상
    video = cv2.VideoCapture('../resources/Examples/cookierun.mp4')
    ################################

    ################################
    # 분석할 이미지   : 에뮬레이터 스크린샷
    # frame = screenshots()
    ################################

    # 프레임 읽기
    ret, frame = video.read()

    ################################
    # 이미지 분석 시작 전 각 종 변수 초기화
    ################################

    sc.read_template()         # 숫자, 젤리 템플릿 읽기

    while not grid.set_grid(frame):     # 최초 화면에서 그리드 위치 찾기
        frame = screenshots()
    print("cookie detected")

    # 프레임 사이즈
    height, width, _ = frame.shape

    ################################
    # 프레임을 분할하기 위한 크기 설정
    ################################
    hx1, hx2, hy1, hy2 = ws.get_health_size(height, width)  # 체력 표시 부분 크기 추출
    sx1, sx2, sy1, sy2 = ws.get_score_size(height, width)   # 점수 표시 부분 크기 추출
    ws.wx1, ws.wx2, ws.wy1, ws.wy2 = ws.get_play_size(height, width)    # 플레이 윈도우 크기 추출
    ws.gx1, ws.gx2, ws.gy1, ws.gy2 = ws.get_ground_size(height, width)  # 바닥 윈도우 크기 추출
    ws.cx1, ws.cx2, ws.cy1, ws.cy2 = ws.get_cookie_size(height, width)  # 쿠키 윈도우 크기 추출

    recent_score, cx, cy, cw, ch = 0, 0, 0, 0, 0     # 선언 및 초기화
    timecheck = time.time()
    level = 1
    while True:
        ################################
        # 프레임 입력 받기 : 예제 동영상
        ret, frame = video.read()
        ################################

        ################################
        # 프레임 입력 받기 : 에뮬레이터 스크린샷
        # frame = screenshots()
        ################################

        # 다음단계로 넘어가는지 디텍션
        if ilu.islevelup(frame,timecheck): # 레벨3까지는 cookiefun_far2 로도 잘 됨 그런데 쿠키 디텍션이 잘 안됨..... tracker를 써야하나
            level += 1
            print('level %d !!'%(level))
            # cv2.putText(frame, "level up!", org=(100, 300), fontFace=1, fontScale=10, color=(255, 0, 0), thickness=5)
            timecheck = time.time()

        # 화면 분할
        score_frame = frame[sy1:sy2, sx1:sx2]  # 점수 표시 부분만 잘라내기
        health_frame = frame[hy1:hy2, hx1:hx2]  # 체력 표시 부분만 잘라내기
        play_frame = frame[ws.wy1:ws.wy2, ws.wx1:ws.wx2]
        ground_frame = frame[ws.gy1:ws.gy2, ws.gx1:ws.gx2]
        cookie_frame = frame[ws.cy1:ws.cy2, ws.cx1:ws.cx2]

        # 정수화
        score, judge = sc.score2int(score_frame)                   # 이미지->정수로 변환
        if not judge:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
            score = recent_score        # 이전의 점수를 그대로 가져오기
        recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 변수 저장
        health = ht.health2int(health_frame, height, width)         # 이미지->체력으로 변환

        # current state matrix
        # 그리드(매트릭스) 초기화 ( 9 * 12 배열 )
        matrix = [[0]*12 for i in range(9)]

        # 각종 개체 리스트 검출
        obstacle_list, jelly_list = ob.obstacle_and_jelly(play_frame)         # 장애물, 젤리 리스트
        ground_list = gd.ground(ground_frame)                       # 바닥 리스트
        cx, cy, cw, ch = ck.cookie(cookie_frame, cx, cy, cw, ch)    # 쿠키

        # 개체 리스트 요소들과 그리드 충돌 검사
        cd.object_collision_detector(matrix, obstacle_list, jelly_list, ground_list)
        cd.cookie_collision(matrix, cx, cy, cw, ch)                  # 쿠키 충돌검사

        ################################
        # 그리드 그리기
        # grid.draw_grid(frame) # 그리드 틀 그리기
        ################################

        ################################
        # 그리드 매트릭스 출력
        for i in range(9):
            print(matrix[i])
        ################################

        # 화면에 체력, 점수 출력
        cv2.putText(frame, str(health), (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(score), (500, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 화면 출력
        cv2.imshow('Cookie', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ################################
    # 입력이 예제 동영상인 경우
    video.release()
    ################################

    cv2.destroyAllWindows()     # 종료시 창 닫기


if __name__ == '__main__':
    main()