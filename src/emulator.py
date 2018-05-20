################################
################################
# 모듈명    : emulator
# 작성자    : 최진호
# 설명      : 에뮬레이터 화면에서 점프, 슬라이드
#             마우스 클릭으로 동작
#             윈도우 환경에서만 사용 가능
################################
################################

import win32api
import win32con


################################
# 함수명    : cookie_jump
# 작성자    : 최진호
# 설명      : 현재 에뮬레이터 화면에서 점프 버튼 위로 마우스 커서를 이동 및 클릭
# 리턴      : _
# 매개변수  : int hgt 에뮬레이터 화면의 높이
#             int wth 에뮬레이터 화면의 너비
################################
def cookie_jump(width, height):
    jump_x = int(width/10)
    jump_y = int(height*9/10)
    win32api.SetCursorPos((jump_x, jump_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


################################
# 함수명    : cookie_slide
# 작성자    : 최진호
# 설명      : 현재 에뮬레이터 화면에서 슬라이드 버튼 위로 마우스 커서를 이동 및 클릭
# 매개변수  : int hgt 에뮬레이터 화면의 높이
#             int wth 에뮬레이터 화면의 너비
################################
def cookie_slide(width, height):
    slide_x = int(width * 8 / 10)
    slide_y = int(height * 9 / 10)
    win32api.SetCursorPos((slide_x, slide_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
