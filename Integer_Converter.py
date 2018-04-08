import cv2


tpl_name_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'B']
tpl_contour_list = []


def read_template():        # 템플릿 읽어오기 (resources 폴더에 저장)
    global tpl_name_list, tpl_contour_list

    for file in tpl_name_list:
        rx = 10000
        img = cv2.imread('resources/' + file + '.png', cv2.IMREAD_COLOR)    # 이미지 읽어오기
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


def health2int(health_frame, height, width):        # 체력 이미지에서 체력 값을 정수로 반환하는 함수

    # 이미지에서 외곽선 찾기위한 필터 적용
    health_blur = cv2.GaussianBlur(health_frame, (3, 3), 0)     # 가우시안 블러 효과 적용
    health_canny = cv2.Canny(health_blur, 150, 200)             # 캐니 효과 적용

    # 체력 값 변환 과정
    ret_health = 0
    _, health_contours, _ = cv2.findContours(health_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    # 모든 외곽선 찾기
    for i in range(len(health_contours)):
        x, y, w, h = cv2.boundingRect(health_contours[i])      # 외곽선의 좌표 반환
        # 체력 외곽선이 좌측 끝에 붙어있고, 기준 높이 이상인 경우에만 진행
        if (h > int(height * 4 / 100)) and (x < int(width * 9 / 100)):
            ret_health = w
    return ret_health


def score2int(score_frame):     # 점수 이미지에서 점수 값을 정수로 반환하는 함수

    # 이미지에서 외곽선 찾아내기 위한 필터 적용
    score_gray = cv2.cvtColor(score_frame, cv2.COLOR_BGR2GRAY)  # 흑백 이미지 전환
    cv2.threshold(score_gray, 127, 255, 0)                      # 흑백 색 대비 강화
    score_blur = cv2.GaussianBlur(score_gray, (5, 5), 0)        # 가우시안 블러 효과 적용
    score_canny = cv2.Canny(score_blur, 190, 220)               # 캐니 효과 적용

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
    if score[0][1] is not 10:       # 점수 외곽선들의 맨 왼쪽 값이 젤리가 아닌 경우
        score_result = 0
        judge = False
    else:                           # 이외의 경우
        score_result = 0
        for i in range(len(score)):         # 점수 배열을 정수 값으로 변환하는 과정
            if score[i][1] is not 10:           # 젤리로 인식되지 않은 경우 (0-9 로 인식)
                score_result *= 10
                score_result += score[i][1]

    return score_result, judge


def get_score_size(height, width):          # 점수 표시 부분의 사이즈 설정
    sx1 = int(width * 70 / 100)
    sx2 = int(width * 95 / 100)
    sy1 = int(height * 1 / 100)
    sy2 = int(height * 7 / 100)
    return sx1, sx2, sy1, sy2


def get_health_size(height, width):         # 체력 표시 부분의 사이즈 설정
    hx1 = int(width * 7 / 100)
    hx2 = int(width * 90 / 100)
    hy1 = int(height * 10 / 100)
    hy2 = int(height * 15 / 100)
    return hx1, hx2, hy1, hy2


def main():        # 메인 함수
    global tpl_name_list, tpl_contour_list          # 전역 변수로 설정
    video = cv2.VideoCapture('cookierun.mp4')
    read_template()         # 템플릿 읽기

    recent_score = 0
    while True:
        ret, frame = video.read()               # 동영상 입력 받기
        height, width, channels = frame.shape   # 동영상의 크기 입력

        # 이미지에서 점수 추출하기
        sx1, sx2, sy1, sy2 = get_score_size(height, width)      # 점수표시부분 크기 추출
        score_frame = frame[sy1:sy2, sx1:sx2]                   # 점수 표시 부분만 잘라내기
        score, judge = score2int(score_frame)                   # 이미지->정수로 변환
        if judge is not True:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
            score = recent_score        # 이전의 점수를 그대로 가져오기
        recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 벼눗 저장

        # 이미지에서 체력 추출하기
        hx1, hx2, hy1, hy2 = get_health_size(height, width)     # 체력표시부분 크기 추출
        health_frame = frame[hy1:hy2, hx1:hx2]                  # 체력 표시 부분만 잘라내기
        health = health2int(health_frame, height, width)        # 이미지->체력으로 변환

        # 이미지에 변환된 값들 출력
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(health), (20, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)     # 체력 출력
        cv2.putText(frame, str(score), (550, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)     # 점수 출력

        cv2.imshow('Cookie', frame)
        cv2.waitKey(10)

    video.release()
    cv2.destroyAllWindows()


main()