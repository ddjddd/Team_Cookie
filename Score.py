import cv2

def score2integer():

    video = cv2.VideoCapture('cookierun.mp4')

    # tpl_name_list = ['resource/1.png']
    tpl_name_list = ['resource/0.png', 'resource/1.png', 'resource/2.png', 'resource/3.png', 'resource/4.png', 'resource/5.png', 'resource/6.png', 'resource/7.png', 'resource/8.png', 'resource/9.png', 'resource/bean.png']
    tpl_contour_list = []

    tag = 0
    for file in tpl_name_list:
        rx = 10000
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thr = cv2.threshold(img_gray, 127, 255, 0)
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
        img_canny = cv2.Canny(img_blur, 100, 200)
        digit_cnt, digit_contours, digit_hierarchy = cv2.findContours(img_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(digit_contours)):
            digit_cnt = digit_contours[i]
            x, y, w, h = cv2.boundingRect(digit_cnt)
            rect_area=w*h
            aspect_ratio = float(w)/h
            if (rect_area >= 100) and (rect_area <= 600):
                if(abs(rx-x) >5):
                    tpl_contour_list.append(digit_contours[i])
                    rx = x
        tag += 1

    while True:
        ret, frame = video.read()        # 동영상 입력 받기
        height, width, channels = frame.shape
        # 점수부분 추출
        score_frame = frame[int(height * 1 / 100):int(height * 7 / 100), int(width * 70 / 100):int(width * 95 / 100)]  # 점수 표시 부분만 잘라내기
        score_gray = cv2.cvtColor(score_frame, cv2.COLOR_BGR2GRAY)
        ret, thr = cv2.threshold(score_gray, 127, 255, 0)
        score_blur = cv2.GaussianBlur(score_gray, (5, 5), 0)
        score_canny = cv2.Canny(score_blur, 190, 220)
        score_cnt, score_contours, score_hierarchy = cv2.findContours(score_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        rx = 0
        score_cnt_list = []
        for i in range(len(score_contours)):
            score_cnt = score_contours[i]
            x, y, w, h = cv2.boundingRect(score_cnt)
            rect_area=w*h
            aspect_ratio = float(w)/h

            if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 150) and (rect_area <= 450):
                if(abs(rx-x) >5):
                    score_cnt_list.append(score_contours[i])
            rx = x
        #
        # zoom = cv2.resize(score_frame, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('Score', zoom)
        # zoom2 = cv2.resize(score_canny, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('Filtered Score', zoom2)

        score = []
        for i in range(len(score_cnt_list)):
            min_res = 100000
            min_id = 0
            for j in range(len(tpl_contour_list)):
                res = cv2.matchShapes(tpl_contour_list[j], score_cnt_list[i], 1, 0.0)
                if min_res > res:
                    min_res = res
                    min_id = j
            x, y, w, h = cv2.boundingRect(score_cnt_list[i])
            score.append((x, min_id))

        score.sort()
        score_result = 0
        for i in range(len(score)):
            if score[i][1] is not 10:
                score_result *= 10
                score_result += score[i][1]
        print(score_result)

        # 체력 게이지 값을 추출하는 과정
        health_frame = frame[int(height * 10 / 100):int(height * 15 / 100), int(width * 7 / 100):int(width * 90 / 100)]
        health_blur = cv2.GaussianBlur(health_frame, (3, 3), 0)
        health_canny = cv2.Canny(health_blur, 150, 200)
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
        cv2.putText(frame, str(len(score_cnt_list)), (450, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(score_result), (550, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Cookie', frame)
        cv2.waitKey(100)

    video.release()
    cv2.destroyAllWindows()


score2integer()