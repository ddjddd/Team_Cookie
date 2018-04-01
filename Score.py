import cv2
import numpy as np

def score2integer():

    video = cv2.VideoCapture('cookierun.mp4')

    # tpl_name_list = ['resource/bean.png']
    tpl_name_list = ['resource/bean.png', 'resource/0.png', 'resource/1.png', 'resource/2.png', 'resource/3.png', 'resource/4.png', 'resource/5.png', 'resource/6.png', 'resource/7.png', 'resource/8.png', 'resource/9.png']
    tpl_contour_list = []

    for file in tpl_name_list:
        img = cv2.imread(file, 0)
        digit_cnt, digit_contours, digit_hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(digit_contours)):
            digit_cnt = digit_contours[i]
            tpl_contour_list.append(digit_cnt)


    while True:
        ret, frame = video.read()        # 동영상 입력 받기

        height, width, channels = frame.shape

        # 점수부분 추출
        score_frame = frame[int(height * 1 / 100):int(height * 7 / 100), int(width * 70 / 100):int(width * 95 / 100)]  # 점수 표시 부분만 잘라내기
        score_blur = cv2.GaussianBlur(score_frame, (3, 3), 0)
        score_canny = cv2.Canny(score_blur, 100, 200)
        score_cnt, score_contours, score_hierarchy = cv2.findContours(score_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(score_contours)):
            score_cnt = score_contours[i]
            x, y, w, h = cv2.boundingRect(score_cnt)
            rect_area=w*h
            aspect_ratio = float(w)/h
            # cv2.drawContours(score_frame, [score_contours[i]], 0, (0, 255, 0), 2)
            if(aspect_ratio >= 0.2)and(aspect_ratio <= 1.0)and(rect_area >= 150)and(rect_area <= 450):
                for idx, tmp in enumerate(tpl_contour_list):
                    res = cv2.matchShapes(score_cnt, tmp, 1, 0.0)
                    print(idx, resab)
                    if res > 9.0:
                        cv2.drawContours(score_frame, [score_contours[i]], 0, (0, 255, 0), 2)



        # 체력 게이지 값을 추출하는 과정
        health_frame = frame[int(height * 10 / 100):int(height * 15 / 100), int(width * 7 / 100):int(width * 90 / 100)]
        health_blur = cv2.GaussianBlur(health_frame, (3, 3), 0)
        health_canny = cv2.Canny(health_blur, 100, 200)
        health_cnt, health_contours, health_hierarchy = cv2.findContours(health_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(health_contours)):
            health_cnt = health_contours[i]
            x, y, w, h = cv2.boundingRect(health_cnt)
            if (h > int(height * 4 / 100))and(x < int(width*9/100)):
                cv2.rectangle(health_frame, (x, y), (x+w, y+h), (255, 255, 255), 5)
                health = w

        # 이미지에 정수로 표현된 체력 값 출력
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(health), (20, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('1', health_frame)
        cv2.imshow('2', health_blur)
        cv2.imshow('3', health_canny)
        cv2.imshow('Score', score_frame)
        cv2.imshow('Filtered Score', score_canny)
        cv2.imshow('Cookie', frame)
        cv2.waitKey(1)

    video.release()
    cv2.destroyAllWindows()


score2integer()