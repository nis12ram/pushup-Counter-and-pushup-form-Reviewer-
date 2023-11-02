import cv2
import mediapipe as mp
from requirefunnc import *

# doing mp setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils

# score variable


video_path = ''
cap = cv2.VideoCapture(video_path)
while True:
    ret, frame = cap.read()
    if (ret != True):
        break
    height, width, _ = frame.shape
    i = 0
    left_Test1Keypoints = []
    right_Test1Keypoints = []

    left_Test2Keypoints = []
    right_Test2Keypoints = []

    scoreleft1 = 0
    scoreright1 = 0

    scoreleft2 = 0
    scoreright2 = 0

    scoreleft3 = 0
    scoreright3 = 0

    scoreleft = 0
    scoreright = 0
    finalscore = 0
    position = ''

    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        # mp_drawing.draw_landmarks(image= output_img,landmark_list=results.pose_landmarks,connections=mp_pose.POSE_CONNECTIONS)
        for list in results.pose_landmarks.landmark:
            #### Test1 keypoints
            if (i == 12 or i == 24 or i == 26):  # right for red
                cv2.circle(frame, (int(list.x * width), int(list.y * height)), 3, (0, 0, 255), -1)
                right_Test1Keypoints.append((int(list.x * width), int(list.y * height)))
            if (i == 11 or i == 23 or i == 25):  # left  for blue
                cv2.circle(frame, (int(list.x * width), int(list.y * height)), 3, (255, 0, 0), -1)
                left_Test1Keypoints.append((int(list.x * width), int(list.y * height)))
            #### Test2 Keypoints
            if (i == 12 or i == 14 or i == 16):  # right for red
                cv2.circle(frame, (int(list.x * width), int(list.y * height)), 5, (0, 0, 255), -1)
                right_Test2Keypoints.append((int(list.x * width), int(list.y * height)))
            if (i == 11 or i == 13 or i == 15):  # left for blue
                cv2.circle(frame, (int(list.x * width), int(list.y * height)), 5, (0, 0, 255), -1)
                left_Test2Keypoints.append((int(list.x * width), int(list.y * height)))

            i += 1
    # if all main keypoints are detected
    if (len(left_Test1Keypoints) != 0 and len(right_Test1Keypoints) != 0 and len(left_Test2Keypoints) != 0 and len(
            right_Test2Keypoints) != 0):
        #### Test 1 Starts (highest score 9)
        print(f'right keypoints are {right_Test1Keypoints}')
        print(f'left keypoints are {left_Test1Keypoints}')
        right_shoulder = right_Test1Keypoints[0]
        right_hip = right_Test1Keypoints[1]
        right_knee = right_Test1Keypoints[2]

        left_shoulder = left_Test1Keypoints[0]
        left_hip = left_Test1Keypoints[1]
        left_knee = left_Test1Keypoints[2]

        # Calculating the distance

        right_sh = int(calculate_distanace_2D(right_shoulder, right_hip))
        right_hk = int(calculate_distanace_2D(right_hip, right_knee))
        right_sk = int(calculate_distanace_2D(right_shoulder, right_knee))

        left_sh = int(calculate_distanace_2D(left_shoulder, left_hip))
        left_hk = int(calculate_distanace_2D(left_hip, left_knee))
        left_sk = int(calculate_distanace_2D(left_shoulder, left_knee))
        print(right_sh, right_sk, right_hk)

        # get the angle
        right_degree_h = get_angle(right_sk, right_sh, right_hk)

        left_degree_h = get_angle(left_sk, left_sh, left_hk)

        print(f'right angle of hip is {right_degree_h}')

        print(f'left angle of hip is {left_degree_h}')

        checkpoint10 = 0
        if (left_degree_h != None):
            left_degree_h = int(left_degree_h)
            for i in range(90, 171, 10):
                checkpoint10 += 1
                # print(f'checkpoint1 is {checkpoint10}')

                if (left_degree_h > i and left_degree_h <= i + 10):
                    scoreleft1 = checkpoint10

        checkpoint11 = 0
        if (right_degree_h != None):
            right_degree_h = int(right_degree_h)
            for i in range(90, 171, 10):
                checkpoint11 += 1
                # print(f'checkpoint1 is {checkpoint11}')
                # print(i)

                if (right_degree_h > i and right_degree_h <= i + 10):
                    scoreright1 = checkpoint11

        print(f'scoreright1 is {scoreright1}')
        print(f'scoreleft1 is {scoreleft1}')

        ### Test1 over

        ### Test2 starts (highest score 10)
        right_shoulder = right_Test2Keypoints[0]
        right_elbow = right_Test2Keypoints[1]
        right_wrist = right_Test2Keypoints[2]

        left_shoulder = left_Test2Keypoints[0]
        left_elbow = left_Test2Keypoints[1]
        left_wrist = left_Test2Keypoints[2]

        right_se = int(calculate_distanace_2D(right_shoulder, right_elbow))
        right_ew = int(calculate_distanace_2D(right_elbow, right_wrist))
        right_sw = int(calculate_distanace_2D(right_shoulder, right_wrist))

        left_se = int(calculate_distanace_2D(left_shoulder, left_elbow))
        left_ew = int(calculate_distanace_2D(left_elbow, left_wrist))
        left_sw = int(calculate_distanace_2D(left_shoulder, left_wrist))

        # calculating right angle
        right_degree_e = get_angle(right_sw, right_se, right_ew)
        print(f'right angle of  elbow is {right_degree_e}')
        # calculating left angle
        left_degree_e = get_angle(left_sw, left_se, left_ew)
        print(f'left angle of elbow  is {left_degree_e}')

        if (left_degree_e != None and right_degree_e != None):
            if (left_degree_e >= 140 and right_degree_e >= 140):
                position = 'up'

            if (left_degree_e <= 125 and right_degree_e <= 125):
                position = 'down'

        checkpoint2 = 10
        if (position == 'up'):
            print(f'x coordinate of right_shoulder is {right_shoulder[0]}')
            print(f'some normalized of right shoulder is {right_shoulder[0] / width * 100}')
            print(f'x coordinate of right_wrist is {right_wrist[0]}')
            print(f'some normalized of right wrist is {right_wrist[0] / width * 100}')
            print(f'x coordinate of left_shoulder is {left_shoulder[0]}')
            print(f'some normalized of left shoulder is {left_shoulder[0] / width * 100}')
            print(f'x coordinate of left_wrist is {left_wrist[0]}')
            print(f'some normalized of keft wrist is {left_wrist[0] / width * 100}')
            x_right_shoulder = right_shoulder[0]
            x_right_shoulder_norm = right_shoulder[0] / width * 100
            x_right_wrist = right_wrist[0]
            x_right_wrist_norm = right_wrist[0] / width * 100

            x_left_shoulder = left_shoulder[0]
            x_left_shoulder_norm = left_shoulder[0] / width * 100
            x_left_wrist = left_wrist[0]
            x_left_wrist_norm = left_wrist[0] / width * 100

            for i in range(0, 10):
                difference = 2 * i
                if (abs(x_right_shoulder_norm - x_right_wrist_norm) >= difference and abs(
                        x_right_shoulder_norm - x_right_wrist_norm) < difference + 2):
                    scoreright2 = checkpoint2
                if (abs(x_left_shoulder_norm - x_left_wrist_norm) >= difference and abs(
                        x_left_shoulder_norm - x_left_wrist_norm) < difference + 2):
                    scoreleft2 = checkpoint2
                checkpoint2 -= 1
        print(f'score right2 is {scoreright2}')
        print(f'score left2 is {scoreleft2}')

        #### Test2 over

        #### Test3 start (highest score 10)

        checkpoint3 = 10
        if (position == 'down'):
            print(f'x coordinate of right_elbow is {right_elbow[0]}')
            print(f'some normalized of  right_elbow is {right_elbow[0] / width * 100}')
            print(f'x coordinate of right_wrist is {right_wrist[0]}')
            print(f'some normalized of right_wrist is {right_wrist[0] / width * 100}')
            print(f'x coordinate of left_elbow is {left_elbow[0]}')
            print(f'some normalized of left_elbow is {left_elbow[0] / width * 100}')
            print(f'x coordinate of left_wrist is {left_wrist[0]}')
            print(f'some noramlized of left_wrist is {left_wrist[0] / width * 100}')

            x_right_elbow = right_elbow[0]
            x_right_elbow_norm = right_elbow[0] / width * 100
            x_right_wrist = right_wrist[0]
            x_right_wrist_norm = right_wrist[0] / width * 100

            x_left_elbow = left_elbow[0]
            x_left_elbow_norm = left_elbow[0] / width * 100
            x_left_wrist = left_wrist[0]
            x_left_wrist_norm = left_wrist[0] / width * 100

            for i in range(0, 10):
                difference = 2 * i
                # print(abs(x_right_elbow - x_right_wrist))
                if (abs(x_right_elbow_norm - x_right_wrist_norm) >= difference and abs(
                        x_right_elbow_norm - x_right_wrist_norm) <= difference + 2):
                    scoreright3 = checkpoint3
                if (abs(x_left_elbow_norm - x_left_wrist_norm) >= difference and abs(
                        x_left_elbow_norm - x_left_wrist_norm) <= difference + 2):
                    scoreleft3 = checkpoint3
                checkpoint3 -= 1

        print(f'score right3 is {scoreright3}')
        print(f'score lef3 is {scoreleft3}')
        #### Test3 over

        #### Final score (highest score 19)
        if (position == "up"):

            if (right_degree_h == None and left_degree_h != None):
                userleftscore = scoreleft1 + scoreleft2
                totalleftscore = 19
                userrightscore = scoreright2

                totalrightscore = 10

                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100

                print(f'right_degree is none final score right is {userrightscore}')
                print(f'right_degree is none final score left is {userleftscore}')
                print(f'right_degree is none final right percent is {scoreright}')
                print(f'right_degree is none final left percent is {scoreleft}')

            elif (left_degree_h == None and right_degree_h != None):
                userleftscore = scoreleft2
                totalleftscore = 10
                userrightscore = scoreright1 + scoreright2
                totalrightscore = 19

                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100

                print(f'left_degree is none final score right is {userrightscore}')
                print(f'left_degree is none final score left is {userleftscore}')
                print(f'left_degree is none final right percent is {scoreright}')
                print(f'left_degree is none final left percent is {scoreleft}')

            elif (left_degree_h == None and right_degree_h == None):
                userleftscore = scoreleft2
                totalleftscore = 10
                userrightscore = scoreright2
                totalrightscore = 10

                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100

                print(f'left_degree and right_degree is none final score right is {userrightscore}')
                print(f'left_degree and right_degree is none final score left is {userleftscore}')
                print(f'left_degree and right_degree is none final right percent is {scoreright}')
                print(f'left_degree and right_degree is none final left percent is {scoreleft}')

            else:
                userleftscore = scoreleft1 + scoreleft2
                userrightscore = scoreright1 + scoreright2
                totalscore = 19
                scoreleft = userleftscore / totalscore * 100
                scoreright = userrightscore / totalscore * 100
                print(f'No angle is None final score right is {userrightscore}')
                print(f'No angle is None final score left is {userleftscore}')
                print(f'No angle is None final right percent is {scoreright}')
                print(f'No angle is None final left percent is {scoreleft}')




        elif (position == "down"):

            if (right_degree_h == None and left_degree_h != None):
                userleftscore = scoreleft1 + scoreleft3
                totalleftscore = 19
                userrightscore = scoreright3
                totalrightscore = 10
                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100
                print(f'right_degree  is None final score right is {userrightscore}')
                print(f'right_degree  is None final score left is {userleftscore}')
                print(f'right_degree  is None final right percent is {scoreright}')
                print(f'right_degree  is None final left percent is {scoreleft}')

            elif (left_degree_h == None and right_degree_h != None):
                userleftscore = scoreleft3
                totalleftscore = 10
                userrightscore = scoreright1 + scoreright3
                totalrightscore = 19
                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100
                print(f'left_degree  is None final score right is {userrightscore}')
                print(f'left_degree  is None final score left is {userleftscore}')
                print(f'left_degree  is None final right percent is {scoreright}')
                print(f'left_degree  is None final left percent is {scoreleft}')

            elif (left_degree_h == None and right_degree_h == None):
                userleftscore = scoreleft3
                totalleftscore = 10
                userrightscore = scoreright3
                totalrightscore = 10
                scoreleft = userleftscore / totalleftscore * 100
                scoreright = userrightscore / totalrightscore * 100
                print(f'left_degree and right_degree  is None final score right is {userrightscore}')
                print(f'left_degree and right_degree  is None final score left is {userleftscore}')
                print(f'left_degree and right_degree  is None final right percent is {scoreright}')
                print(f'left_degree and right_degree  is None final left percent is {scoreleft}')


            else:
                userleftscore = scoreleft1 + scoreleft3
                userrightscore = scoreright1 + scoreright3
                totalscore = 19
                scoreleft = userleftscore / totalscore * 100
                scoreright = userrightscore / totalscore * 100
                print(f'No angle is None final score right is {userrightscore}')
                print(f'No angle is None final score left is {userleftscore}')
                print(f'No angle is None final right percent is {scoreright}')
                print(f'No angle is None final left percent is {scoreleft}')

        if (position == 'up' or position == 'down'):
            finalscore = int((scoreright + scoreleft) / 2)

            print(f'Form correctness is around {finalscore}')
            cv2.putText(frame, f'Form accuracy {finalscore} %', (10, 20), 1, 2, (0, 0, 255), 2)

        else:
            if (left_degree_h != None and right_degree_h != None):
                userscore = scoreleft1 + scoreright1
                totalscore = 18
                finalscore = int((userscore / totalscore) * 100)

            print(f'Form correctness is around {finalscore}')
            cv2.putText(frame, f'Form accuracy {finalscore} %', (10, 20), 1, 2, (0, 0, 255), 2)
    else:
        print(f'Model is not able to detect all of the desired keypoints')

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if (key == 27):
        break

cap.release()
cv2.destroyAllWindows()
