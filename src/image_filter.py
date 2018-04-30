import cv2


def make_canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 그레이 스케일 화면으로 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0)        # 가우시안 블러 필터 적용
    canny = cv2.Canny(blur, 110, 200)               # 캐니효과 적용
    return canny
