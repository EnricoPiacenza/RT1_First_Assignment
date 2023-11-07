from __future__ import print_function
from timeit import default_timer as timer
import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear dist"""

d_dh = 0.6
"""float: Threshold for the control of relative position with target token"""

rot_direction = 1
"""Integer: Threshold to control the sense of rotation of the robot to find the next token"""

tokens_grabbed = []
""" List that traks the tokens already moved in the desired position"""

target_token = 0
""" Code of the token used to collect the others"""
next_to_grab = 0
""" Code of the next nearest token to grab and collect"""

R = Robot()

def reach_token(code,dist):
    """ 
    Function to reach the desired token
    Args: code (int): code of the token we want to reach
          dist (float): dist we want to stop the robot from the desired token         
    """

    print("Reaching token number: " + str(code) + "...") 

    while(True):
        d, angl = find_token(code)
        if(d == -1 or angl == -1):
            turn(rot_direction*40,0.1)
        elif(d < dist):
            return
        elif angl > a_th:
            turn(5,0.1)
        elif angl < -a_th:
            turn(-5,0.1)
        else:
            drive(50,0.1)

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
    Function to find the desired token
    Args: code (int): code of the token we want to reach

    Returns:
        dist (float): dist of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """

    dist = 100
    
    for token in R.see():
        if token.info.code == code:
            dist = token.dist
            rot_y = token.rot_y
            break
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

def find_nearest():
    
    """
    Function to find the closest token to the robot that is yet to collect

    Returns:
        code (int): the code of the nearest token found (-1 if no token is detected)        
    """

    global rot_direction
    global next_to_grab

    dist = 100
    code = 0
    t_0 = timer()
    ideal = "clockwise"
    print("Searching for the nearest token...")
    while 1:
        turn(40,0.1)  
        for token in R.see():
            if token.dist < dist and token.info.code not in tokens_grabbed:
                dist = token.dist
                code = token.info.code
                t_t = timer()
                if(t_t - t_0 < 1.6):
                    rot_direction = 1
                else:
                    rot_direction = -1
                    ideal = "counterclockwise"                

        t_1 = timer()
        if(t_1 - t_0 >= 3.15):
            break
    if(dist == 100):
        next_to_grab = -1
    else:
        print("--> Token code: " + str(code) + " dist: " + str(round(dist,2)) + " Delta time: " + str(round(t_t-t_0,2)) + " Most efficient sense of rotation: " + ideal)
        next_to_grab = code

def find_furthest():

    global next_to_grab

    dist = 0
    code = 0
    t_0 = timer()
    ideal = "clockwise"
    print("Searching for the further token...")
    while 1:
        turn(40,0.1)  
        for token in R.see():
            if token.dist > dist and token.info.code not in tokens_grabbed:
                dist = token.dist
                code = token.info.code
                t_t = timer()
                if(t_t - t_0 < 1.6):
                    rot_direction = 1
                else:
                    rot_direction = -1
                    ideal = "counterclockwise"                

        t_1 = timer()
        if(t_1 - t_0 >= 3.15):
            break
    if(dist == 100):
        next_to_grab = -1
        return -1
    else:
        print("--> Token code: " + str(code) + " dist: " + str(round(dist,2)) + " Delta time: " + str(round(t_t-t_0,2)) + " Most efficient sense of rotation: " + ideal)
        next_to_grab = code
        return dist


def collect_nearest():
    """
        function to reach and grab the nearest token
    """
    
    reach_token(next_to_grab,d_th)
    R.grab()
    


def bring_back_nearest():
    """
        function to bring back the collected token near the target one.
    """

    global rot_direction

    rot_direction *= -1
    reach_token(target_token,d_dh)
    if R.release():
        tokens_grabbed.append(next_to_grab)
        drive(-30,1)


def def_target_token():

    global target_token

    find_nearest()
    if(next_to_grab == -1):
        print("Error, no token detected.")
        exit()
    reach_token(next_to_grab,d_th)    
    R.grab()
    tokens_grabbed.append(next_to_grab)
    target_token = next_to_grab

    print("Target token: " + str(target_token))

def def_collecting_area():

    dist = find_furthest()
    reach_token(next_to_grab,dist/2)
    R.release()
    drive(-30,1)



def grab_all_tokens():

    while 1:

        find_nearest()

        if next_to_grab == -1:
            print("All tokens were collected")
            #exit()
            break

        collect_nearest()
        bring_back_nearest()
        print("Tokens collected: " + str(tokens_grabbed))

def main():
    t_0 = timer()
    def_target_token()
    def_collecting_area()
    grab_all_tokens()
    t_1 = timer()

    print("Time necessary to collect all tokens: " + str(round(t_1-t_0,2)) + " seconds.")



main()