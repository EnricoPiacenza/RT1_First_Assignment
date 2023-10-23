from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

d_dh = 0.6
"""float: Threshold for the control of relative position with target token"""

tokens_grabbed = []
""" list that traks the already moved"""

target_token = 0
""" code of the token used to collect the others"""

R = Robot()

def reach_token(code,d_th):

    while(True):
        dist, angl = find_token(code)
        if(dist == -1 or angl == -1):
            print("no token detected")
            turn(20,0.1)
        elif(dist < d_th):
            return
        elif angl > a_th:
            turn(5,0.1)
        elif angl < -a_th:
            turn(-5,0.1)
        else:
            drive(30,0.1)

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0    

def find_token(code):
    """
    Function to find the closest token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code == code:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

def find_nearest():
    nearest = 33
    code = 0
    while nearest == 33:

        turn(-20,0.1)  
        for token in R.see():
            if token.dist < nearest and token.info.code not in tokens_grabbed:
                nearest = token.dist
                code = token.info.code

    return code


def collect_nearest(token):
    
    reach_token(token,d_th)
    R.grab()
    tokens_grabbed.append(token)


def bring_back_nearest():

    reach_token(target_token,d_dh)
    R.release()   
    drive(-30,1)


def setup_target_token():
    global target_token

    code = find_nearest()
    reach_token(code,d_th)    
    R.grab()
    tokens_grabbed.append(code)
    target_token = code

    print("Target token: " + str(target_token))
    
    code = find_nearest()
    reach_token(code,d_dh)
    tokens_grabbed.append(code)
    R.release()
    drive(-30,1)



def grab_all_tokens():

    while len(tokens_grabbed) != 6:
        token_code = find_nearest()
        print("next nearest: " + str(token_code))
        collect_nearest(token_code)
        bring_back_nearest()
        print("Tokens collected: " + str(tokens_grabbed))
    print("All token were collected")




setup_target_token()
grab_all_tokens()
