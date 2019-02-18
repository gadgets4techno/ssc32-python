#!/usr/bin/python3
#-*- coding: utf-8 -*-

# SSC-32 Python implementation
# for CapTechU robot arm
# Adapted from https://bitbucket.org/vooon/pyssc32
import arm,script
from time import sleep

test="/home/techno/scriptV2.csv"
#c=c.controller(None,115200)
s=None
robot=arm.Arm(arm.c)
home=False
joypad=False

def call(servo=None,pos=None,pwm=None,**kwargs):
    print(servo,pos,pwm)
    for key,val in kwargs.items():
        if key == "home":
            print("Homing arm...",val)
    pass

def init():
    global s
    if arm.c.board.is_open == False:
        arm.c.connect()    #Port will be opened if successful
    robot.highArm.home=2500
    s=script.Script(test,call)
    pass


def main():
    print("Welcome to Chinese Controller for SSC-32")
    init()
    #center()
    print(s.filename,s.file,s.file.is_file())
    s.run()
    raise KeyboardInterrupt
   
    pass

# Center all servos
def center():
    print("Homing arm...\n")
    for a in robot.parts:
        a.goHome()
        #a.position=a.home
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sleep(0.1)
        arm.c.close()
        #center()
