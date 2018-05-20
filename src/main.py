import cv2

import numpy as np
import time
from PIL import ImageGrab
from src.detectors import obstacles_and_jelly as ob, score as sc, ground as gd, health as ht, cookie as ck, collision_detector as cd, is_level_up as ilu
from src import window_size as ws
from src import grid
from termcolor import colored
import sys

monitor = ImageGrab.grab()
monitor = np.array(monitor)[:, :, ::-1].copy()
monitor = monitor.shape[0]
monitor =int (monitor/40)


def screenshots():
    box = (0, monitor, 852, 480+monitor)
    im = ImageGrab.grab(box)#.convert('RGB')
    frame = np.array(im)[:, :, ::-1].copy()
    return frame

# 메인 함수
def main():

    frame = screenshots()
    sc.read_template()         # 템플릿 읽기



    while not grid.detect_first(frame):# 최초 화면에서 그리드 위치 찾기
        frame = screenshots()

    print("cookie detected")

    height, width, channels = frame.shape  # 동영상의 크기 입력
    hx1, hx2, hy1, hy2 = ws.get_health_size(height, width)
    sx1, sx2, sy1, sy2 = ws.get_score_size(height, width)  # 점수표시부분 크기 추출

    ws.wx1, ws.wx2, ws.wy1, ws.wy2 = ws.get_play_size(height, width)  # 플레이 윈도우 크기 설정
    ws.gx1, ws.gx2, ws.gy1, ws.gy2 = ws.get_ground_size(height, width)
    ws.cx1, ws.cx2, ws.cy1, ws.cy2 = ws.get_cookie_size(height, width)

    recent_score, cx, cy, cw, ch = 0, 0, 0, 0, 0     # 선언 및 초기화
    timecheck = time.time()
    level = 1
    while True:

        frame = screenshots()
       
        # 다음단계로 넘어가는지 디텍션
        if ilu.islevelup(frame,timecheck): # 레벨3까지는 cookiefun_far2 로도 잘 됨 그런데 쿠키 디텍션이 잘 안됨..... tracker를 써야하나
            level += 1
            print('level %d !!'%(level)) #cv2.putText(frame, "level up!", org=(100, 300), fontFace=1, fontScale=10, color=(255, 0, 0), thickness=5)
            timecheck = time.time()


        # ret, frame = video.read()               # 동영상 입력 받기

        ################################
        # 매트릭스 작성
        ################################
        score_frame = frame[sy1:sy2, sx1:sx2]  # 점수 표시 부분만 잘라내기
        health_frame = frame[hy1:hy2, hx1:hx2]  # 체력 표시 부분만 잘라내기
        play_frame = frame[ws.wy1:ws.wy2, ws.wx1:ws.wx2]
        ground_frame = frame[ws.gy1:ws.gy2, ws.gx1:ws.gx2]
        cookie_frame = frame[ws.cy1:ws.cy2, ws.cx1:ws.cx2]

        ################################
        # 정수화
        ################################

        score, judge = sc.score2int(score_frame)                   # 이미지->정수로 변환
        if not judge:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
            score = recent_score        # 이전의 점수를 그대로 가져오기
        recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 변수 저장

        health = ht.health2int(health_frame, height, width)         # 이미지->체력으로 변환

        ################################
        # 개체 리스트 작성
        ################################
        matrix = [[0]*12 for i in range(9)]

        # 이미지에서 장애물 추출하기
        obstacle_list, jelly_list = ob.obstacle(play_frame)
        cd.obstacle_collision(matrix, obstacle_list)
        cd.jelly_collision(matrix, jelly_list)

        # 이미지에서 바닥 추출하기
        ground_list = gd.ground(ground_frame)
        cd.ground_collision(matrix, ground_list)

        # 이미지에서 쿠키 추출하기
        cx, cy, cw, ch = ck.cookie(cookie_frame, cx, cy, cw, ch)
        cd.cookie_collision(matrix, cookie_frame, cx, cy, cw, ch)                  # 쿠키 충돌검사

        # 그리드 그리기
        grid.draw_grid(frame)
        gridstring=''
        for i in range(9):
            for j in range(12):
                value = matrix[i][j]
                if value == 1:
                    color = 'yellow'
                elif value == 7:
                    color = 'blue'
                elif value == 4 or value == 3:
                    color = 'red'
                elif value == 0 :
                    color = 'white'
                print(colored(value, color), end='   ')
                #gridstring+= str(value)+"   "
            print()
            #gridstring+="\n"
        #for i in range(10):
            #sys.stdout.write("\033[K")
        #print(gridstring)
        print("-----------------------------------------------")




        cv2.putText(frame, str(health), (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(score), (500, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Cookie', frame)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    #video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
     main()

    # frame = screenshots()
    # cv2.imshow('crop', frame)
    # cv2.waitKey(0)