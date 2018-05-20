################################
################################
# 모듈명    : health
# 작성자    : 최진호
# 설명      : 분할된 체력 화면에서 체력 게이지를 인식하고 정수로 변환
################################
################################

import cv2
from src import image_filter as imf


################################
# 함수명    : health2int
# 작성자    : 최진호
# 설명      : 분할된 체력 화면에서 체력 게이지를 인식하고 정수로 변환
# 리턴      : int health 검출된 체력
# 매개변수  : image health_frame 분할된 체력 화면
#             int height 전체 화면 높이
#             int width 전체 화면 너비
################################
def health2int(health_frame, height, width):
    health_canny = imf.make_canny(health_frame) # 이미지에서 외곽선 찾기위한 필터 적용

    # 체력 값 변환 과정
    health = 0      # 선언 및 초기화
    _, health_contours, _ = cv2.findContours(health_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    # 모든 외곽선 찾기
    for i in range(len(health_contours)):
        x, y, w, h = cv2.boundingRect(health_contours[i])      # 외곽선의 좌표 반환
        # 체력 외곽선이 좌측 끝에 붙어있고, 기준 높이 이상인 경우에만 진행
        if (h > int(height * 4 / 100)) and (x < int(width * 9 / 100)):
            health = w

    return health
