import cv2
from src import image_filter as imf

tpl_name_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'B']
tpl_contour_list = []


# 템플릿 읽어오기 (resources 폴더에 저장)
def read_template():
    global tpl_name_list, tpl_contour_list

    for file in tpl_name_list:
        rx = 10000
        img = cv2.imread('../resources/Templates/' + file + '.png', cv2.IMREAD_COLOR)    # 이미지 읽어오기
        img_blur = cv2.GaussianBlur(img, (3, 3), 0)                 # 가우시안 블러 효과 적용
        img_canny = cv2.Canny(img_blur, 100, 200)                   # 캐니 효과 적용
        _, digit_contours, _ = cv2.findContours(img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    # 모든 외곽선 찾기

        # 모든 외곽선 대상으로 검사
        for i in range(len(digit_contours)):
            x, y, w, h = cv2.boundingRect(digit_contours[i])
            rect_area = w * h

            # 외곽선의 넓이가 기준치 이상인 경우에만 템플릿으로 인정
            if (rect_area >= 100) and (rect_area <= 600):
                if abs(rx - x) > 5:     # 기존에 선택한 외관선 값과 좌표차이가 기준치 이상인 경우에만 점수 자릿수로 인정
                    tpl_contour_list.append(digit_contours[i])  # 템플릿 외곽선 배열에 현재 외곽선 값을 저장
                    rx = x          # 기준치 검사를 위한 변수 저장


# 점수 이미지에서 점수 값을 정수로 반환하는 함수
def score2int(score_frame):
    score_gray = cv2.cvtColor(score_frame, cv2.COLOR_BGR2GRAY)  # 흑백 이미지 전환
    # 이미지에서 외곽선 찾아내기 위한 필터 적용
    score_canny = imf.make_canny(score_frame)

    # 외곽선 찾아내고 정수로 전환하기 위한 검사
    _, score_contours, _ = cv2.findContours(score_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 모든 외곽선 찾기
    rx = 0
    score_cnt_list = []
    for i in range(len(score_contours)):    # 모든 외곽선 집함베 대하여 검사
        x, y, w, h = cv2.boundingRect(score_contours[i])    # 현재 점수 외곽선의 좌표 받아오기
        rect_area = w * h               # 외곽선의 넓이
        aspect_ratio = float(w) / h     # 외관선의 너비-높이 비율

        # 비율, 넓이의 기준치에 도달하는 외관선들만 선택
        if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 150) and (rect_area <= 450):
            if abs(rx - x) > 5:     # 기존에 선택한 외관선 값과 좌표차이가 기준치 이상인 경우에만 점수 자릿수로 인정
                score_cnt_list.append(score_contours[i])    # 점수 외곽선 배열에 현재 외곽선 값을 저장
        rx = x      # 기준치 검사를 위한 변수 저장

    # 위에서 저장된 점수 외곽선의 배열에서 각각의 정수값을 검출하는 과정
    score = []  # 각 외관선에서 추출된 정수값과 관련된 정보를 위한 배열 선언
    for i in range(len(score_cnt_list)):    # 각각의 점수 컨투어에 대해 검사
        min_res = 100000
        min_id = 0
        for j in range(len(tpl_contour_list)):      # 0-9, 젤리에 대한 템플릿에 대하여 검사
            res = cv2.matchShapes(tpl_contour_list[j], score_cnt_list[i], 1, 0.0)   # res 값이 낮을수록 정확도 증가
            if min_res > res:       # 최소의 res 값 선정
                min_res = res
                min_id = j
        x, y, w, h = cv2.boundingRect(score_cnt_list[i])    # 현재 점수 외곽선의 좌표 받아오기

        # 예외 처리 과정
        if min_id is 7 or min_id is 1:
            if w <= 10:
                min_id = 1
            else:
                min_id = 7
        elif min_id is 6 or min_id is 9:
            if score_gray[y + int(h * 8 / 10), x + int(w / 4)] > 200:
                min_id = 6
            else:
                min_id = 9
        elif min_id is 0 or min_id is 2 or min_id is 3 or min_id is 5:
            if score_gray[y + int(h / 2), x + int(w / 5)] > 200:
                min_id = 0
            else:
                if score_gray[y + int(h * 2 / 5), x + int(w * 2 / 5)] > 200:
                    min_id = 5
                else:
                    if score_gray[y + int(h * 3 / 5), x + int(w * 2 / 5)] > 200:
                        min_id = 2
                    else:
                        min_id = 3

        score.append((x, min_id))   # 점수 배열에 현재 외곽선의 값 추가

    score.sort()        # 점수 외곽선들을 왼쪽부터 순서대로 정렬

    judge = True
    score_result = 0
    for i in range(len(score)):         # 점수 배열을 정수 값으로 변환하는 과정
        if score[i][1] is not 10:           # 젤리로 인식되지 않은 경우 (0-9 로 인식)
            score_result *= 10
            score_result += score[i][1]

    return score_result, judge
