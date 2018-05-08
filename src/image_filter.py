################################
################################
# 모듈명    : image_filter
# 작성자    : 최진호
# 설명      : 입력된 이미지를 흑백->블러->캐니 효과 적용
################################
################################

import cv2


################################
# 함수명    : make_canny
# 작성자    : 최재필
# 설명      : 입력된 이미지를 흑백->블러->캐니 효과 적용
# 리턴      : image input_image 필터링된 이미지
# 매개변수  : image canny 이미지
################################
def make_canny(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)  # 그레이 스케일 화면으로 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0)        # 가우시안 블러 필터 적용
    canny = cv2.Canny(blur, 110, 200)               # 캐니효과 적용

    return canny
