#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Script interpreter for custom commands
import csv
from pathlib import Path
from time import sleep

class Script(object):
    _data=["$"]
    _hash=["#"]
    _home=["HOME"]
    _go=["GO"]
    _wait=["WAIT",{0}]
    def __init__(self,filepath,callback):
        self.file=Path(filepath)  # Script location
        #self._dir=None  # Directory of filename
        self.commands=None
        self.callback=callback
        self.use_pwm=True
        self.cmds=["GO","#","WAIT","HOME","OFFSET","$"]
        #self.cfgs={"UNITS":["DEGREES","POSITION"],"TIME":["S","MS"],"PORT":None}
        pass

    @DeprecationWarning("Use run() instead")
    def open(self):
        with open(str(self.file),newline='') as f:
            self.commands=csv.reader(f,delimiter=",")
            for each in self.commands:
                print(each)
            return self.commands

    def saveL(self,line):
        if type(line) == tuple or type(line) == list:
                try:
                    with open(self.file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(line)
                        return True
                except:
                    return False
        else:
            return False
        pass

    def configure(self):
        pass

    def run(self):
        servos=None
        with open(str(self.file),newline='') as f:
            self.commands=csv.reader(f,delimiter=",")    
            for arg in self.commands:
                if str(arg[0]).startswith(self.cmds[1]):    # (#) Do nothing
                    continue
                else:
                    if str(arg[0]).startswith(self.cmds[0]):    # (GO) to position with servos
                        del arg[0]
                        servos=arg
                        continue
                    elif str(arg[0]).startswith(self.cmds[5]):  # ($) Get positions and "set" them
                        del arg[0]
                        for s,p in zip(servos,arg):
                            self.callback(s,p,self.use_pwm)
                    elif str(arg[0]).startswith(self.cmds[3]):  # Go (HOME)
                        self.callback(home=True)
                    elif str(arg[0]).startswith(self.cmds[2]):  # (WAIT) before next command
                        sleep(int(arg[1])/1000)
                        #self.callback(wait=arg[1])
        pass

    @property
    def filename(self):
        return self.file

    @filename.setter
    def filename(self,name):
        self.file=Path(name)
        if self.file.is_file() == False:
            return False
        pass
    pass