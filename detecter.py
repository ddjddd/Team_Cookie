import cv2

def score2integer():

    video = cv2.VideoCapture('img/cookierun.mp4')

    # tpl_name_list = ['resource/3.png']
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
        digit_cnt, digit_contours, digit_hierarchy = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(digit_contours)):
            digit_cnt = digit_contours[i]
            x, y, w, h = cv2.boundingRect(digit_cnt)
            rect_area=w*h
            if (rect_area >= 100) and (rect_area <= 500):
                if(abs(rx-x) >5):
                    tpl_contour_list.append(digit_contours[i])
                    cv2.drawContours(img, [digit_contours[i]], 0, (0, 0, 255), 1)
                    rx = x
        # zoom = cv2.resize(img, None, fx = 4, fy =4, interpolation=cv2.INTER_CUBIC)
        # cv2.imshow(tpl_name_list[tag], zoom)
        tag += 1

    score_frame = cv2.imread('sources/d1.png', cv2.IMREAD_COLOR)
    score_gray = cv2.cvtColor(score_frame, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(score_gray, 127, 255, 0)
    score_blur = cv2.GaussianBlur(score_gray, (5, 5), 0)
    score_canny = cv2.Canny(score_blur, 190, 220)
    score_cnt, score_contours, score_hierarchy = cv2.findContours(score_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    rx = 10000000
    score_cnt_list = []
    for i in range(len(score_contours)):
        score_cnt = score_contours[i]
        x, y, w, h = cv2.boundingRect(score_cnt)
        rect_area = w * h
        aspect_ratio = float(w) / h

        if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 150) and (rect_area <= 450):
            if (abs(rx - x) > 5):
                score_cnt_list.append(score_contours[i])
        rx = x

    score = []
    for i in range(len(score_cnt_list)):
        min_res = 100000
        for j in range(len(tpl_contour_list)):
            res = cv2.matchShapes(tpl_contour_list[j], score_cnt_list[i], 1, 0.0)
            if min_res > res:
                min_res = res
                min_id = j
            print(j, res)
        print()
        x, y, w, h = cv2.boundingRect(score_cnt_list[i])
        score.append((x, min_id))

    score.sort()
    score_result = 0
    for i in range(len(score)):
        if score[i][1] is not 10:
            score_result *= 10
            score_result += score[i][1]
    print(score_result)

    zoom = cv2.resize(score_frame, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Score', zoom)
    zoom2 = cv2.resize(score_canny, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Filtered Score', zoom2)

    cv2.imshow('Cookie', score_frame)
    cv2.waitKey(0)


score2integer()