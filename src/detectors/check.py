import cv2

tpl_name_list = ['check', 'open_all', 'start']
tpl_list=[]

def read_template():
    global tpl_name_list

    for file in tpl_name_list:
        tpl = cv2.imread('../../resources/Templates/' + file + '.png', cv2.IMREAD_GRAYSCALE)
        tpl_list.append(tpl)


def main():
    video = cv2.VideoCapture('../../resources/Examples/check.mp4')

    # 프레임 읽기
    ret, frame = video.read()

    # 프레임 사이즈
    height, width, _ = frame.shape



    while True:
        ret, frame = video.read()
        max_v = 0
        cur_tpl = -1
        for i in range(len(tpl_list)):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray, tpl_list[i], cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > max_v:
                max_v = max_val
                if max_v > 0.99:
                    w, h = tpl_list[i].shape[::-1]
                    cur_tpl = i
                    top_left = max_loc
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv2.rectangle(frame, top_left, bottom_right, 255, 2)


        cv2.imshow('video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()     # 종료시 창 닫기

read_template()
main()