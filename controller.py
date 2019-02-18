#!/usr/bin/python3

#Interface for Prolific Servo controller
#SSC-32 running on ATmega168
# Version = SSC32-V2.04GP

import serial
from ports import ports
from servo import Servo

class controller(ports):
    version="SSC32-V2.04GP "  # The return string from the controller
    def __init__(self,port=None,baud=None,channels=32,auto=1000):
        self.board=serial.Serial()
        self.board.baudrate=baud
        self.board.port=port
        self.board.timeout=1
        self.auto=auto
        self.myversion=""
        self._servos = [Servo(self._servo_on_changed, i, "servo"+str(i)) for i in range(channels)]

    def __getitem__(self, it):
        if type(it) == str:# or type(it) == unicode
            for servo in self._servos:
                it = it.upper()
                if servo.name == it:
                    return servo
            raise KeyError(it)
        return self._servos[it]

    def _servo_on_changed(self):
        if self.auto is not None:
            self.update(self.auto)

    def update(self,time=None):
        cmd = ''.join([self._servos[i]._get_cmd_string() for i in range(len(self._servos))])
        if time is not None and cmd != '':
            cmd += 'T{0}'.format(time)
        cmd += '\r'
        print(cmd.encode())
        self.board.write(cmd.encode())
        pass

    def close(self):
        self.board.close()
        
    def checkPort(self):
        if self.board.port != None:
            try:
                self.board.open()
                if not self.verCheck():
                    self.board.close()
                    return False
                else:
                    return True
            except:
                return False
#
#           else:
#             d=ports().getPort()    #returns list
#             #print(len(d))
# 
#             for each in d:
#                 try:
#                     print(each)
#                     self.board.port=each
#                     self.board.open()
#                     if not self.verCheck():
#                         self.board.close()
#                         break
#                 except:
#                     return None

    def connect(self):
        if not self.checkPort():
            self.board.open()
        self.board.flush()
        pass

    def verCheck(self,reportStr=False):
        self.board.write("VER \r".encode())
        v=bytes(self.board.readline())
        v=v.decode()
        v=v.strip()
        #print(type(v),len(v),v)
        if v not in self.version:
            print("Weird software version: "+v)
            if reportStr == False:
                return False
            else:
                return v
        else:
            print("Software version OK: "+v)
            if reportStr == False:
                return True
            else:
                return v
        pass

    def cancel(self):
        cmd="#\r"   #\u
        self.board.write(cmd.encode())

    def home(self,time=None): #set arm to home position
        cmd = ''.join([self._servos[i]._getHome() for i in range(len(self._servos))])
        if time is not None and cmd != '':
            cmd += 'T{0}'.format(time)
        cmd += '\r'
        self.board.write(cmd.encode())
        pass

    # Set offset for channel
    # Should run only once
    # Value = (-100) - 100
    def setOffset(self,channel,value):
        cmd="#{0}PO{1}".format(channel,value)
        cmd += '\r'
        self.board.write(cmd.encode())
        pass

    def isDone(self):
        self.board.flushInput()
        self.board.write('Q\r'.encode())
        r = self.board.read(1)
        return r == '.'

    def move(self,channel,pos,speed=None,time=None):
        pass