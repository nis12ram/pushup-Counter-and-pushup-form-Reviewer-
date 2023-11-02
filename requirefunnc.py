import math
import pyttsx3
import threading
import  time


def calculate_distanace_3D(point1, point2):
    x1, y1, z1 = int(point1[0]), int(point1[1]), int(point1[2])
    x2, y2, z2 = int(point2[0]), int(point2[1]), int(point2[2])

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return distance


def calculate_distanace_2D(point1, point2):
    x1, y1 = int(point1[0]), int(point1[1])
    x2, y2 = int(point2[0]), int(point2[1])

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def get_angle(opp_distance, adj_distance1, adj_distance2):
    numerator = ((adj_distance1) ** 2) + ((adj_distance2) ** 2) - ((opp_distance) ** 2)
    denominator = 2 * (adj_distance1) * (adj_distance2)
    if (denominator != 0):
        cos_e = numerator / denominator
        if (-1 <= cos_e <= 1):
            radian_e = math.acos(cos_e)
            degree_e = (180 / math.pi) * radian_e
            return degree_e
        else:
            print(f'cos_e value is {cos_e} exceeds the range fo -1 and 1')
            return None
    else:
        print(f'side value si {adj_distance1, adj_distance2}')
        return None


def speak(word):
    engine = pyttsx3.init()
    # engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(word)
    engine.runAndWait()





def automaticTerminate(count, count_lst,ret):

    checker = 0

    if len(count_lst) > 300:
        for i in range(1, 301):
            if (count_lst[-i] == count):
                checker += 1
    if (checker == 300 and ret == True):
        task2 = threading.Thread(target=speak, args=[
            f'Total push up done is {count}. Thanks for choosing me Signing off from my  side'])
        task2.start()

        raise Exception("Breaking the code 1")
    if (ret == False):
        time.sleep(2)

        task3 = threading.Thread(target=speak, args=[
            f'Total push up done is {count}. Thanks for choosing me Signing off from my  side'])
        task3.start()

        raise Exception("Breaking the code 2")


