#!/usr/bin/python3

# Robot file specifically for 
# Lynxmotion AL5D
import controller,servo
c=controller.controller("/dev/ttyACM0",115200)
#d=controller.controller("/dev/ttyUSB1",115200)
class Arm():
    def __init__(self,p):
        # Servo channel definitions
        self.base=p["servo0"]
        self.lowArm=p["servo1"]
        self.highArm=p["servo2"]
        self.wrist=p["servo3"]
        self.wristr=p["servo4"]
        self.hand=p["servo5"]
        self.parts=(self.base,self.lowArm,self.highArm,self.wrist,self.wristr,self.hand)
        pass