#!/usr/bin/python3

#Serial port lister

import sys,glob,serial

class ports():
  def __init__(self):
    pass

  def send(self,data):
      pass

  def sendReturn(self):
      pass

  def getPort(self):
    print("Your platform is: ", end="")
    #Windows
    if sys.platform.startswith('win'):
      print("Windows")
      ports = ['COM%s' % (i+1) for i in range(256)]
    #GNU/Linux
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
      print("GNU/LINUX")
      ports = glob.glob('/dev/tty[A-Za-z]*')
    #Mac
    elif sys.platform.startswith('darwin'):
      print("Not worth mentioning...")
      ports=glob.glob('/dev/tty*')
    #unsupported platform
    else:
      print("UNK/No Support")
      #  raise EnvironmentError('Unsupported platform')
      ports=None
      return ports

    result=[]
    for port in ports:
      try:
        s=serial.Serial(port)
        s.close()
        result.append(port)
      except (OSError, serial.SerialException):
        pass
    return result

if __name__ == "__main__":
 pass
 print(ports().getPort())
