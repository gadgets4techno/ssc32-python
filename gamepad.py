#!/usr/bin/python

# Gamepad handler

import glob
from time import sleep
from evdev import *
name1="Sony PLAYSTATION(R)3 Controller"
name2="Xbox Gamepad (userspace driver)"
pad=None
pads=glob.glob('/dev/input/event*')

def find():
    global pad
    for pad in pads:
        gamepad=InputDevice(pad)
        print(gamepad.name)
        if gamepad.name in (name1,name2):
            pad=InputDevice(pad)
            break
    pass

def list():
    pass

if __name__ == "__main__":
 find()
 for event in pad.read_loop():
     print(categorize(event))     
     sleep(0.01)