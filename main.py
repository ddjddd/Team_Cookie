import cv2
import integer_converter as ic


def main():        # 메인 함수
    video = cv2.VideoCapture('resources/Examples/cookierun.mp4')
    ic.read_template()         # 템플릿 읽기

    recent_score = 0
    while True:
        ret, frame = video.read()               # 동영상 입력 받기
        height, width, channels = frame.shape   # 동영상의 크기 입력

        # 이미지에서 점수 추출하기
        sx1, sx2, sy1, sy2 = ic.get_score_size(height, width)      # 점수표시부분 크기 추출
        score_frame = frame[sy1:sy2, sx1:sx2]                      # 점수 표시 부분만 잘라내기
        score, judge = ic.score2int(score_frame)                   # 이미지->정수로 변환
        if judge is not True:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
            score = recent_score        # 이전의 점수를 그대로 가져오기
        recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 벼눗 저장

        # 이미지에서 체력 추출하기
        hx1, hx2, hy1, hy2 = ic.get_health_size(height, width)      # 체력표시부분 크기 추출
        health_frame = frame[hy1:hy2, hx1:hx2]                      # 체력 표시 부분만 잘라내기
        health = ic.health2int(health_frame, height, width)         # 이미지->체력으로 변환

        # 이미지에 변환된 값들 출력
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(health), (20, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)     # 체력 출력
        cv2.putText(frame, str(score), (550, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)     # 점수 출력

        cv2.imshow('Cookie', frame)
        cv2.waitKey(10)

    video.release()
    cv2.destroyAllWindows()


main()