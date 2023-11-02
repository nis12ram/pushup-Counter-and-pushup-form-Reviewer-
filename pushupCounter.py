import cv2
import mediapipe as mp
from requirefunnc import *
import threading

import time

# doing mp setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils

video_path = ''
cap = cv2.VideoCapture(video_path)

count = 0
position = ''
permit = 1

count_lst = []

speak(
    "hi i am your ai assistant.  i will count your push up and notify your total value at the end and also i will close the code automatically.   so let's start your fitness journey")
try:
    while True:
        count_lst.append(count)

        i = 0
        left_keypoints = []
        right_keypoints = []

        ret, frame = cap.read()
        automaticTerminate(count, count_lst, ret)

        height, width, _ = frame.shape

        if (ret != True):
            break

        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            for list in results.pose_landmarks.landmark:
                if (i == 11 or i == 13 or i == 15):  # blue for left
                    cv2.circle(frame, (int(list.x * width), int(list.y * height)), 3, (255, 0, 0), -1)
                    left_keypoints.append((int(list.x * width), int(list.y * height)))
                elif (i == 12 or i == 14 or i == 16):  # green for right
                    cv2.circle(frame, (int(list.x * width), int(list.y * height)), 3, (0, 255, 0), -1)
                    right_keypoints.append((int(list.x * width), int(list.y * height)))
                i += 1

        print(f'left keypoints are {left_keypoints}')
        print(f'right keypoints are {right_keypoints}')

        if (len(left_keypoints) != 0 and len(right_keypoints) != 0):
            left_shoulder = left_keypoints[0]
            left_elbow = left_keypoints[1]
            left_wrist = left_keypoints[2]

            right_shoulder = right_keypoints[0]
            right_elbow = right_keypoints[1]
            right_wrist = right_keypoints[2]

            # Calculating the distance for angle measurement 2D

            left_se_2D = int(calculate_distanace_2D(left_shoulder, left_elbow))
            left_ew_2D = int(calculate_distanace_2D(left_elbow, left_wrist))
            left_sw_2D = int(calculate_distanace_2D(left_shoulder, left_wrist))

            right_se_2D = int(calculate_distanace_2D(right_shoulder, right_elbow))
            right_ew_2D = int(calculate_distanace_2D(right_elbow, right_wrist))
            right_sw_2D = int(calculate_distanace_2D(right_shoulder, right_wrist))

            print(f'left_se_2D is {left_se_2D}')
            print(f'left_ew_2D is {left_ew_2D}')
            print(f'left_sw_2D is {left_sw_2D}')
            print(f'right_se_2D is {right_se_2D}')
            print(f'right_ew_2D is {right_ew_2D}')
            print(f'right_sw_2d is {right_sw_2D}')

            # calculating left angle
            left_degree_e = get_angle(left_sw_2D, left_se_2D, left_ew_2D)
            print(f'left angle is {left_degree_e}')

            # calculating right angle
            right_degree_e = get_angle(right_sw_2D, right_se_2D, right_ew_2D)
            print(f'right angle is {right_degree_e}')

            # processng the counter form
            if (left_degree_e != None and right_degree_e != None):
                if (permit == 1):
                    if (left_degree_e >= 155 and right_degree_e >= 155):
                        position = 'up'
                        permit = 0

                if (permit == 0):

                    if (left_degree_e <= 125 and right_degree_e <= 125):
                        position = 'down'
                        permit = 1
                        count += 1
                        # speak(f'{count}')
                        task1 = threading.Thread(target=speak, args=[f'{count}'])
                        task1.start()

            cv2.putText(frame, f'Count  {count}', (10, 20), 1, 1.5, (20, 20, 255), 2)
            cv2.putText(frame, f'Position {position}', (10, 50), 1, 1.5, (20, 20, 255), 2)

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)

            if (key == 27):
                break
except Exception as e:
    print(f'Exception is {e}')

time.sleep(3)

cap.release()
cv2.destroyAllWindows()
