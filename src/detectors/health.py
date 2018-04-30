import cv2
from src import image_filter as imf


# 체력 이미지에서 체력 값을 정수로 반환하는 함수
def health2int(health_frame, height, width):
    # 이미지에서 외곽선 찾기위한 필터 적용
    health_canny = imf.make_canny(health_frame)
    # 체력 값 변환 과정
    ret_health = 0
    _, health_contours, _ = cv2.findContours(health_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    # 모든 외곽선 찾기
    for i in range(len(health_contours)):
        x, y, w, h = cv2.boundingRect(health_contours[i])      # 외곽선의 좌표 반환
        # 체력 외곽선이 좌측 끝에 붙어있고, 기준 높이 이상인 경우에만 진행
        if (h > int(height * 4 / 100)) and (x < int(width * 9 / 100)):
            ret_health = w
    return ret_health
