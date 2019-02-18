#!/usr/bin/python3
#-*- coding: utf-8 -*-

# SSC-32 Python implementation
# for CapTechU robot arm
# Adapted from https://bitbucket.org/vooon/pyssc32
import arm
import itertools
from time import sleep

#c=c.controller(None,115200)
robot=arm.Arm(arm.c)
robot2=arm.Arm(arm.d)
home=False
joypad=False

def init():
    if arm.c.board.is_open == False:
        arm.c.connect()    #Port will be opened if successful
    if arm.d.board.is_open == False:
        arm.d.connect()
    robot.highArm.home=2500
    robot2.highArm.home=2500
    pass


def main():
    print("Welcome to Chinese Controller for SSC-32")
    init()
    center()
    raise KeyboardInterrupt

    while(1):
        center()
        sleep(2)
    #    #stepAll()
    #    #sleep(2)
        stepOne()
        sleep(2)
    
    pass

# Center all servos
def center():
    print("Homing arm...\n")
    for a, b in zip(robot.parts, robot2.parts):
        a.position=a.home
        b.position=b.home
        #each.position=each.home
        sleep(1)
        
# Iteratively rotate each
def stepOne():
    print("Rotating joints...\n")
    for a,b in zip(robot.parts, robot2.parts):
        for pos in range(-90,90):
        #for pos in range(500,2500):
            a.degrees=pos
            b.degrees=pos
            sleep(0.05)
        a.position=a.home
        b.position=b.home

# Iteratively move all servos        
def stepAll():
    print("Doing the robot...\n")
    for pos in range(-90,90):
        for each in robot.parts:
            each.degrees=pos
            sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sleep(0.1)
        center()
