import cv2
import numpy as np
import time
from PIL import ImageGrab

from src import window_size as ws, grid
from src.detectors import obstacles_and_jelly as ob, score as sc, ground as gd, health as ht, cookie as ck
from src.detectors import collision_detector as cd, is_level_up as ilu
from termcolor import colored
import emulator

import numpy as np
import random

import sys

import tensorflow as tf
from my_gym import gym
from dqn import dqn
from collections import deque

#####
# 듀얼 모니터 등 컴퓨터의 디스플레이 세팅값 다르면 읽어와서 맞춤.
#####
from ctypes import windll

user32 = windll.user32
user32.SetProcessDPIAware()


monitor = ImageGrab.grab()
monitor = np.array(monitor)[:, :, ::-1].copy()
monitor = monitor.shape[0]
monitor = int(monitor/28)


################################
# 함수명    : screenshots
# 작성자    : 이석범
# 설명      : 현재 에뮬레이터에서 화면을 스크린샷(캡처)
# 리턴      : image 캡처된 화면
# 매개변수  :  _
################################
def screenshots():
    box = (0, monitor, 852, 480+monitor)
    im = ImageGrab.grab(box)    # .convert('RGB')
    frame = np.array(im)[:, :, ::-1].copy()
    return frame


################################
# 함수명    : main
# 작성자    : _
# 설명      : _
# 리턴      : _
# 매개변수  : _
################################

env = gym

input_size = env.input_size
output_size = len(env.action_space)

dis = 0.9
REPLAY_MEMORY = 50
max_episodes = 100


def replay_train(mainDQN, targetDQN, train_batch):
    x_stack = np.empty(0).reshape(0, input_size)
    y_stack = np.empty(0).reshape(0, output_size)

    # Get stored information from the buffer
    for state, action, reward, next_state, done in train_batch:
        Q = mainDQN.predic(state)

        # terminal?
        if done:
            Q[0, action] = reward
        else:
            # get target from target DQN (Q')
            Q[0, action] = reward + dis * np.max(targetDQN.predict(next_state))

        y_stack = np.vstack([y_stack, Q])
        x_stack = np.vstack( [x_stack, state])

    # Train our network using target and predicted Q values on each episode
    return mainDQN.update(x_stack, y_stack)

def ddqn_replay_train(mainDQN, targetDQN, train_batch):
    '''
    Double DQN implementation
    :param mainDQN: main DQN
    :param targetDQN: target DQN
    :param train_batch: minibatch for train
    :return: loss
    '''
    x_stack = np.empty(0).reshape(0, mainDQN.input_size)
    y_stack = np.empty(0).reshape(0, mainDQN.output_size)
    # Get stored information from the buffer
    for state, action, reward, next_state, done in train_batch:
        Q = mainDQN.predict(state)

        # terminal?
        if done:
            Q[0, action] = reward
        else:
            # Double DQN: y = r + gamma * targetDQN(s')[a] whereimpo
            # a = argmax(mainDQN(s'))
            Q[0, action] = reward + dis * targetDQN.predict(next_state)[0, np.argmax(mainDQN.predict(next_state))]

        y_stack = np.vstack([y_stack, Q])
        x_stack = np.vstack([x_stack, state])

    # Train our network using target and predicted Q values on each episode
    return mainDQN.update(x_stack, y_stack)

def simple_replay_train(mainDQN, train_batch):
    '''
    Simple DQN implementation
    :param mainDQN: main DQN
    :param train_batch: minibatch for train
    :return: loss
    '''
    x_stack = np.empty(0).reshape(0, mainDQN.input_size)
    y_stack = np.empty(0).reshape(0, mainDQN.output_size)

    # Get stored information from the buffer
    for state, action, reward, next_state, done in train_batch:
        Q = mainDQN.predict(state)

        # terminal?
        if done:
            Q[0, action] = reward
        else:
            # Double DQN: y = r + gamma * targetDQN(s')[a] where
            # a = argmax(mainDQN(s'))
            Q[0, action] = reward + dis * np.max(mainDQN.predict(next_state))

        y_stack = np.vstack([y_stack, Q])
        x_stack = np.vstack([x_stack, state])

    # Train our network using target and predicted Q values on each episode
    return mainDQN.update(x_stack, y_stack)

def get_copy_var_ops(*, dest_scope_name="target", src_scope_name="main"):

    # Copy variables src_scope to dest_scope
    op_holder = []

    src_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
    dest_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)

    for src_var, dest_var in zip(src_vars, dest_vars):
        op_holder.append(dest_var.assign(src_var.value()))

    return op_holder

def bot_play(mainDQN, isTest=False):
    # See our trained network in action in test env
    state = env.reset(isTest)
    # start = state[2]
    reward_sum = 0
    while True:
        #env.render()
        action = np.argmax(mainDQN.predict(state))
        state, reward, done, _ = env.step(action)
        reward_sum += reward
        if done:
            print("\t{} based profit : {}".format("Test" if isTest else "Train", reward_sum))
            break





replay_buffer = deque()



def main():


    ################################
    # 분석할 이미지   : 동영상
    #video = cv2.VideoCapture('../resources/Examples/cookierun.mp4')
    # 프레임 읽기
    #ret, frame = video.read()
    ################################

    ################################
    # 분석할 이미지   : 에뮬레이터 스크린샷
    frame = screenshots()
    ################################



    ################################
    # 이미지 분석 시작 전 각 종 변수 초기화
    ################################

    sc.read_template()         # 숫자, 젤리 템플릿 읽기

    while not grid.set_grid(frame):     # 최초 화면에서 그리드 위치 찾기
        frame = screenshots()
    print("cookie detected")

    # 프레임 사이즈
    height, width, _ = frame.shape

    ################################
    # 프레임을 분할하기 위한 크기 설정
    ################################
    hx1, hx2, hy1, hy2 = ws.get_health_size(height, width)  # 체력 표시 부분 크기 추출
    sx1, sx2, sy1, sy2 = ws.get_score_size(height, width)   # 점수 표시 부분 크기 추출
    ws.wx1, ws.wx2, ws.wy1, ws.wy2 = ws.get_play_size(height, width)    # 플레이 윈도우 크기 추출
    ws.gx1, ws.gx2, ws.gy1, ws.gy2 = ws.get_ground_size(height, width)  # 바닥 윈도우 크기 추출
    ws.cx1, ws.cx2, ws.cy1, ws.cy2 = ws.get_cookie_size(height, width)  # 쿠키 윈도우 크기 추출

    recent_score, cx, cy, cw, ch = 0, 0, 0, 0, 0     # 선언 및 초기화
    timecheck = time.time()
    level = 1


    with tf.Session() as sess:
        mainDQN = dqn.DQN(sess, input_size, output_size, name="main")
        targetDQN = dqn.DQN(sess, input_size, output_size, name="target")
        tf.global_variables_initializer().run()

        #initial copy q_net -> target_net
        copy_ops = get_copy_var_ops(dest_scope_name="target", src_scope_name="main")
        sess.run(copy_ops)

        for episode in range(max_episodes):
            e = 1. / ((episode / 10) + 1)
            done = False
            step_count = 0
            state = env.reset()
            reward_sum = 0

            before_action = True

            while not done:
                ################################
                # 프레임 입력 받기 : 예제 동영상
                # ret, frame = video.read()
                ################################

                ################################
                # 프레임 입력 받기 : 에뮬레이터 스크린샷
                frame = screenshots()
                ################################

                # 다음단계로 넘어가는지 디텍션
                if ilu.islevelup(frame,timecheck): # 레벨3까지는 cookiefun_far2 로도 잘 됨 그런데 쿠키 디텍션이 잘 안됨..... tracker를 써야하나
                    level += 1
                    print('level %d !!'%(level))
                    # cv2.putText(frame, "level up!", org=(100, 300), fontFace=1, fontScale=10, color=(255, 0, 0), thickness=5)
                    timecheck = time.time()

                # 화면 분할
                score_frame = frame[sy1:sy2, sx1:sx2]  # 점수 표시 부분만 잘라내기
                health_frame = frame[hy1:hy2, hx1:hx2]  # 체력 표시 부분만 잘라내기
                play_frame = frame[ws.wy1:ws.wy2, ws.wx1:ws.wx2]
                ground_frame = frame[ws.gy1:ws.gy2, ws.gx1:ws.gx2]
                cookie_frame = frame[ws.cy1:ws.cy2, ws.cx1:ws.cx2]

                # 정수화
                score, judge = sc.score2int(score_frame)                   # 이미지->정수로 변환
                if not judge:           # 점수 컨투어의 맨 왼쪽 컨투어가 젤리가 아닌 경우
                    score = recent_score        # 이전의 점수를 그대로 가져오기
                recent_score = score            # 현재 점수를 다음 프레임으로 전달하기 위한 변수 저장
                health = ht.health2int(health_frame, height, width)         # 이미지->체력으로 변환

                # current state matrix
                # 그리드(매트릭스) 초기화 ( 9 * 12 배열 )

                matrix = [[0]*12 for i in range(9)]

                # 각종 개체 리스트 검출
                obstacle_list, jelly_list = ob.obstacle_and_jelly(play_frame)         # 장애물, 젤리 리스트
                ground_list = gd.ground(ground_frame)                       # 바닥 리스트
                cx, cy, cw, ch = ck.cookie(cookie_frame, cx, cy, cw, ch)    # 쿠키

                # 개체 리스트 요소들과 그리드 충돌 검사
                cd.object_collision_detector(matrix, obstacle_list, jelly_list, ground_list)
                cd.cookie_collision(matrix, cx, cy, cw, ch)                  # 쿠키 충돌검사

                ################################
                # 그리드 그리기q
                grid.draw_grid(frame) # 그리드 틀 그리기
                grid.fill_grid(frame, matrix)   # 그리드 채우기
                ################################

                ################################
                # 그리드 매트릭스 출력
                for i in range(9):

                    for j in range(12):
                        value = matrix[i][j]
                        if value == 1:
                            color = 'yellow'
                        elif value == 2:
                            color = 'blue'
                        elif value == -1 or value == -2:
                            color = 'red'
                        elif value == 0 :
                            color = 'white'
                        print(colored(value, color), end='   ')
                        #gridstring+= str(value)+"   "
                    print()
                print("-----------------------------------------------")
                print('step', step_count)
                print("health", health)
                print('score', score)


                state = np.array([np.array(matrix).flatten()])
                if np.random.rand(1) < e:
                    action = random.sample(env.action_space, 1)[0]
                else:
                    # Choose an action by greedily from the Q-network
                    action = np.argmax(mainDQN.predict(state))


                # step
                if before_action == True:

                    if action == 0:  #####JUMP
                        emulator.cookie_jump(852, 480)
                        before_action = -1* before_action
                        before_score = score
                        continue

                    elif action == 1:  #####SLIDE
                        emulator.cookie_slide(852, 480)
                        before_action = -1 * before_action
                        before_score = score
                        continue

                    elif action == 2:  ####DO NOTHING
                        emulator.cookie_donothing(852, 480)
                        before_action = -1 * before_action
                        before_score = score
                        continue

                done = True if (health < 5) else False

                reward = score - before_score

                # next_state, reward, done, _ = env.step(action)
                reward_sum += reward

                next_state = state

                # Save the experience to our buffer
                replay_buffer.append((state, action, reward, next_state, done))

                if len(replay_buffer) > REPLAY_MEMORY:
                    replay_buffer.popleft()

                step_count += 1

                before_action = True



                # 화면에 체력, 점수 출력
                cv2.putText(frame, str(health), (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, str(score), (500, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # 화면 출력
                cv2.imshow('Cookie', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    ################################
    # 입력이 예제 동영상인 경우
    # video.release()
    ################################

    cv2.destroyAllWindows()     # 종료시 창 닫기


if __name__ == '__main__':
    main()