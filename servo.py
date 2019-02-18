#!/usr/bin/python3

#Servo object class

class Servo():
    def __init__(self,on_changed_callback,id,name="F"):
        self.name = name.upper()
        self.id = id
        self.min = 500#100  #500
        self.max = 2500#1500 #2500
        self._pos = 1500
        self.home = 1500
        self.deg_min = -90.0
        self.deg_max = 90.0
        self.is_changed = False
        #This is a func reference
        self.on_changed_callback = on_changed_callback

    def __repr__(self):
        if self.name is not None:
            name = ' '+self.name
        else:
            name = ''
        return '<Servo{0}: #{1} pos={2}({5}°) {3}({6}°)..{4}({7}°)>'.format(
            name, self.id, self._pos, self.min, self.max,
            self.degrees, self.deg_min, self.deg_max)
    
    @property
    def position(self):
        return self._pos
    
    @position.setter
    def position(self, pos):
        """
        Set absolute position
        """
        pos = int(pos)
        if pos > self.max:
            pos = self.max
        elif pos < self.min:
            pos = self.min

        self.is_changed = True
        self._pos = pos        
        # Execute function
        self.on_changed_callback()

    @property
    def degrees(self):
        deltapos = self._pos - self.min
        return self.deg_min + \
                (abs(self.deg_min)*deltapos + abs(self.deg_max)*deltapos) \
                / (self.max - self.min)

    @degrees.setter
    def degrees(self,deg):
        #set in degrees
        deg=float(deg)
        pos = self.min + \
                (deg - self.deg_min) * (self.max - self.min) \
                / (abs(self.deg_min) + abs(self.deg_max))
        self.position = pos

    def _get_cmd_string(self):
        if self.is_changed:
            self.is_changed = False
            return '#{0}P{1}'.format(self.id, self._pos)
        else:
            return ''

    def _getHome(self):
        return '#{0}P{1}'.format(self.id, self.home)

    def goHome(self):
        self.position=self.home
