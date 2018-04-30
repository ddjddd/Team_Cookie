import pyscreenshot as ImageGrab
import cv2
import numpy as np

from src.detectors import obstacles as ob, score as sc, ground as gd, health as ht
from src import window_size as ws


def screenshots():
    x1 = 0
    x2 = 830
    y1 = 40
    y2 = 510
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_np = np.array(img)
    return img_np


# 메인 함수
def main():
    video = cv2.VideoCapture('../resources/Examples/cookierun.mp4')
    sc.read_template()         # 템플릿 읽기

    recent_score = 0
    while True:
        ret, frame = video.read()               # 동영상 입력 받기
        # frame = screenshots()
        height, width, channels = frame.shape   # 동영상의 크기 입력

        # print(height, width)

        # 이미지에서 점수 추출하기
        sx1, sx2, sy1, sy2 = ws.get_score_size(height, width)      # 점수표시부분 크기 추출
        score_frame = frame[sy1:sy2, sx1:sx2]                      # 점수 표시 부분만 잘라내기
        score, judge = sc.score2int(score_frame)                   # 이미지->정수로 변환
        if judge is not True:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
            score = recent_score        # 이전의 점수를 그대로 가져오기
        recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 벼눗 저장

        # 이미지에서 체력 추출하기
        hx1, hx2, hy1, hy2 = ws.get_health_size(height, width)      # 체력표시부분 크기 추출
        health_frame = frame[hy1:hy2, hx1:hx2]                      # 체력 표시 부분만 잘라내기
        health = ht.health2int(health_frame, height, width)         # 이미지->체력으로 변환

        # 이미지에서 장애물 추출하기
        wx1, wx2, wy1, wy2 = ws.get_play_window_size(height, width)
        play_frame = frame[wy1:wy2, wx1:wx2]
        ob.obstacle(play_frame, wy2 - wy1, wx2 - wx1)
        # cv2.imshow('roi', roi_frame)

        wx1, wx2, wy1, wy2 = ws.get_ground_size(height, width)
        ground_frame = frame[wy1:wy2, wx1:wx2]
        gd.ground(ground_frame)
        # gd.ground(frame)

        cv2.putText(frame, str(health), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(score), (550, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Cookie', frame)
        cv2.waitKey(0)

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
     main()

    # frame = screenshots()
    # cv2.imshow('crop', frame)
    # cv2.waitKey(0)