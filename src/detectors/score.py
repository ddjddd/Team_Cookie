################################
################################
# 모듈명    : score
# 작성자    : 최진호
# 설명      : 분할된 점수 화면에 점수를 인식하고 정수로 변환
################################
################################

import cv2
from src import image_filter as imf

# 전역 변수 선언 및 초기화
tpl_name_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'B']
tpl_contour_list = []
score_before=0

################################
# 함수명    : read_template
# 작성자    : 최진호
# 설명      : 템플릿 비교에 사용될 템플릿 읽기
#             [0~9] + [기본젤리]
# 리턴      : _
# 매개변수  : _
################################
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


################################
# 함수명    : score2int
# 작성자    : 최진호
# 설명      : 점수화면에서 숫자 검출 -> 정수화
# 리턴      : int score 검출된 점수
#             Boolean Judge 기본젤리 인식 여부
# 매개변수  : image score_frame 분할된 점수 화면
################################
def score2int(score_frame):
    score_gray = cv2.cvtColor(score_frame, cv2.COLOR_BGR2GRAY)  # 흑백 이미지 전환
    # 이미지에서 외곽선 찾아내기 위한 필터 적용
    score_canny = imf.make_canny(score_frame)

    # 외곽선 찾아내고 정수로 전환하기 위한 검사
    _, score_contours, _ = cv2.findContours(score_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 모든 외곽선 찾기
    rx = 0
    score_cnt_list = []
    for i in range(len(score_contours)):    # 모든 외곽선 집합에 대하여 검사
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

    global score_before

    judge = True
    score_result = 0

    for i in range(len(score)):         # 점수 배열을 정수 값으로 변환하는 과정
        if score[i][1] is not 10:           # 젤리로 인식되지 않은 경우 (0-9 로 인식)
            score_result *= 10
            score_result += score[i][1]

    #직전의 점수 상태와 새로 도출한 점수를 비교하는 과정
    if(score_before!=0):
        if(score_before<=score_result):
            if(score_result-score_before>40000):    #숫자의 증가폭이 4만점 이상이면 잘못 인식된 점수로 간주
                score_result=score_before           #새 점수를 점수에 반영하지 않는다
        else:          #새로운 점수가 이전의 점수보다 오히려 줄어든 경우 역시 점수 인식이 잘못된 상황
            score_result=score_before

    score_before=score_result

    return score_result, judge
