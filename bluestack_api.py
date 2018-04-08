import win32api
import win32con


def cookie_jump(width, height):
    jump_x = int(width/10)
    jump_y = int(height*9/10)
    win32api.SetCursorPos((jump_x, jump_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    return


def cookie_slide(width, height):
    slide_x = int(width * 8 / 10)
    slide_y = int(height * 9 / 10)
    win32api.SetCursorPos((slide_x, slide_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    return