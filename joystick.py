#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Joystick handler
import inputs,threading
from time import sleep

class Joystick(object):
    def __init__(self):
        self._pad=None
        self.connected=True
        self._run=True
        self.available=[]
        self.strings=['Sync',"Misc","Absolute","Key"]
        pass

    def __getitem__(self,index):
        if type(index) != int:
            raise TypeError("list index not in range")
        else:
            return self.available[index]
        pass

    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self,id):
        if type(id)==int:
            print("int controller id")
            #self.connected=False
            self._pad=id
            #self.connected=True
        pass

    def find(self):
        self.available=inputs.devices.gamepads
        if len(self.available) > 0:
            return True
        else:
            return False
        pass

    def _get(self):
        if self.connected == True:
            try:
                events = inputs.devices.gamepads[self._pad]
                f=events.read() 
                #return f
                for e in f:
                   if e.ev_type != "Sync":
                       #if e.ev_type != "Absolute":
                           #return(e)
                        return([e.ev_type,e.code,e.state])
            except Exception as e:
                print("Failed try", e, e.args)
                #self.connected=False
                #return False
                return(["0","0","0"])
        else:
            print("Failed if statement")
            return(["0","0","0"])
            #return False
    pass

class Generic(Joystick):    # When you don't know your controller type or don't care
    def __init__(self,id):
        super().__init__()
        self._buttons={"BTN_SOUTH":0,"BTN_EAST":0,"BTN_NORTH":0,
        "BTN_WEST":0,"BTN_SELECT":0,"BTN_START":0,
        "BTN_MODE":0,"BTN_TL":0,"BTN_TR":0,"BTN_THUMBL":0,
        "BTN_THUMBR":0}   # Keys
        self.SOUTH=self._buttons["BTN_SOUTH"]
        self.EAST=self._buttons["BTN_EAST"]
        self.NORTH=self._buttons["BTN_NORTH"]
        self.WEST=self._buttons["BTN_WEST"]
        self.TL=self._buttons["BTN_TL"]
        self.TR=self._buttons["BTN_TR"]
        self.THUMBL=self._buttons["BTN_THUMBL"]
        self.THUMBR=self._buttons["BTN_THUMBR"]
        self.SELECT=self._buttons["BTN_SELECT"]
        self.START=self._buttons["BTN_START"]
        self.MODE=self._buttons["BTN_MODE"]
        
        self.hats={"D_UP":0,"D_DOWN":0,"D_LEFT":0,"D_RIGHT":0}
        self.D_UP=self.hats["D_UP"]   # Absolute
        self.D_DOWN=self.hats["D_DOWN"]
        self.D_LEFT=self.hats["D_LEFT"]
        self.D_RIGHT=self.hats["D_RIGHT"]
        self.hat=["ABS_HAT0X","ABS_HAT0Y"]
        self._sticks={"ABS_X":0,"ABS_Y":0,"ABS_RX":0,"ABS_RY":0}
        self.STICKS={"X":self._sticks["ABS_X"],"Y":self._sticks["ABS_Y"],"RX":self._sticks["ABS_RX"],"RY":self._sticks["ABS_RY"]}
        
        self._triggers={"ABS_Z":0,"ABS_RZ":0}
        self.TRIGGERS={"Z":self._triggers["ABS_Z"],"RZ":self._triggers["ABS_RZ"]}

        self.find()
        self.pad=id
        self.t=threading.Thread(target=self.update)
        self.t.setDaemon(True)
        pass

    def update(self):
        while(self._run):
            g=self._get()
            #print("Update:",type(g),g)
            if g != None:
                if g[0] == self.strings[3]:  #"Keys"
                    
                    if g[1] in self._buttons.keys():  # Buttons
                        self.convertButton(g[1],g[2])

                elif g[0] == self.strings[2]:  #"Absolute"
                    #print("Update:",type(g),g)
                    if g[1] in self.hat: # D-Pad/HAT
                        self.convertHat(g[1],g[2])

                    elif g[1] in self._sticks.keys():   # Sticks
                        self.convertSticks(g[1],g[2])

                    elif g[1] in self._triggers.keys():  # Triggers
                        self.convertTriggers(g[1],g[2])
                    
            #sleep(0.005)
            pass
        #return

    def convertHat(self,code,val):
        if code == self.hat[0]:
            if val == -1:
                self.hats["D_LEFT"]=1
                self.hats["D_RIGHT"]=0
            elif val == 0:
                self.hats["D_LEFT"]=0
                self.hats["D_RIGHT"]=0
            elif val == 1:
                self.hats["D_LEFT"]=0
                self.hats["D_RIGHT"]=1
        elif code == self.hat[1]:
            if val == -1:
                self.hats["D_UP"]=1
                self.hats["D_DOWN"]=0
            elif val == 0:
                self.hats["D_UP"]=0
                self.hats["D_DOWN"]=0
            elif val == 1:
                self.hats["D_UP"]=0
                self.hats["D_DOWN"]=1
        pass

    def convertButton(self,code,val):
        self._buttons[code]=val
        pass
    
    def convertSticks(self,code,val):
        self._sticks[code]=val
        pass

    def convertTriggers(self,code,val):
        self._triggers[code]=val
        pass

class Xbox(Generic):
    def __init__(self,id):
        super().__init__(id)
        self.A=self.SOUTH
        self.B=self.EAST
        self.X=self.NORTH
        self.Y=self.WEST
        self.LB=self.TL
        self.RB=self.TR
        self.VIEW=self.SELECT
        self.MENU=self.START
        self.XBOX=self.MODE
        self.xtriggers={"LT":self.TRIGGERS["Z"],"RT":self.TRIGGERS["RZ"]}
        pass

class PlayStation(Generic):
    def __init__(self,id):
        super().__init__(id)
        self.ps_strings=["ABS_X","ABS_Y","ABS_RZ","ABS_Z"]
        self.sixaxis=["ABS_MT_DISTANCE","ABS_MT_TOOL_Y","ABS_MT_TOOL_X",
        "ABS_MT_TOUCH_MINOR","ABS_MT_TOUCH_MAJOR",]
        self._ps_buttons={"BTN_TRIGGER_HAPPY1":0,"BTN_TRIGGER":0,"BTN_TOP":0,"BTN_BASE3":0,
        "BTN_BASE4":0,"BTN_BASE5":0,"BTN_BASE6":0,"BTN_DEAD":0}
        self.CROSS=self.SOUTH   #notImplemented
        self.CIRCLE=self.EAST   #notImplemented
        self.SQUARE=self._ps_buttons["BTN_DEAD"]
        self.TRIANGLE=self.WEST #notImplemented
        self.L1=self._ps_buttons["BTN_BASE5"]
        self.R1=self._ps_buttons["BTN_BASE6"]
        self.L3=self.THUMBL
        self.R3=self.THUMBR
        self.PS=self.MODE
        self.hats={"BTN_BASE":0,"BTN_BASE2":0,"BTN_PINKIE":0,"BTN_TOP":0}
        self.D_UP=self.hats["BTN_TOP"]
        self.D_DOWN=self.hats["BTN_BASE"]
        self.D_LEFT=self.hats["BTN_BASE2"]
        self.D_RIGHT=self.hats["BTN_PINKIE"]
        self.PS=self._ps_buttons["BTN_TRIGGER_HAPPY1"]
        self.SELECT=self._ps_buttons["BTN_TRIGGER"]
        self.START=self._ps_buttons["BTN_TOP"]
        self.ltriggers={"L2":self._ps_buttons["BTN_BASE3"],"R2":self._ps_buttons["BTN_BASE4"]}
        self.lsticks={"L3_X":self.STICKS["X"],"L3_Y":self.STICKS["Y"],"R3_X":self.STICKS["RX"],"R3_Y":self.STICKS["RY"]}
        pass

    def update(self):
        while(self._run):
            g=self._get()
            if type(g) == bool:
                pass
            if g!= None:
                if g[0] == self.strings[3]: #"Keys"
                    pass
                elif g[0] == self.strings[2]:
                    if g[1] in self.ps_strings:
                        print("PSUpdate:",type(g),g)

if __name__ == "__main__":
    #p=Xbox(1)
    p=PlayStation(0)
    #threading.Thread(target=x.update).start()
    p.t.start()
    try:
        print("class id's",p.pad,p.available,str(p.available[0]))
        #print(p.)
        while(1):
            #print(p._buttons,p._sticks,p._triggers,p.hats)
            sleep(1)
            #raise Exception
    except:
        print("Quitting...")
        p._run=False
        p.t.join()
        
    print(p.t.is_alive())