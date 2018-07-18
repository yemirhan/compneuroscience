from __future__ import division
from tkinter import *
from emokit.emotiv import Emotiv
from collections import deque
from scipy import signal, fft
from Queue import Queue
import time
import threading
import sys
import os
import os.path
class Reader(threading.Thread):
    def __init__(self,q1,flag1,step,tw,electrodes):
        super(Reader, self).__init__()
        self.Fs=128
        self._stop = threading.Event()
        self.q1=q1
        self.flag1=flag1
        self.step=step
        self.tw=tw*self.Fs
        self.electrodes=electrodes
    def stop(self):
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()
    def run(self):
        O1_buff = ring_buffer(self.tw)
        i=0
        #old=0
        #old2=0
        with Emotiv(display_output=False, verbose=True, write=False) as headset:
            try:
                while not self._stop.isSet():
                    packet = headset.dequeue()
                    if packet is not None:
                        i=i+1
                        data=[]
                        readtime = time.time()
                        for name in electrodes.split(' '):
                            data.append([packet.sensors[name]['value'],packet.sensors[name]['quality']])
                        O1_buff.write(data)
                        #writeData(data)#cogs lab addition
                        file.write(str(data)+ " :" + str(readtime) + "\n")  # cogs lab addition
                        #print data
                        #print(time.time()-old)
                        #old=time.time()
                        pass
                    if i==self.step:
                        self.flag1.set()
                        self.q1.put(O1_buff.list_ret())
                        self.flag1.clear()
                        i=0
                        #print(time.time()-old2)
                        #old2=time.time()
            except :
                pass


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
if __name__ == '__main__':
      
      root = Tk()
   elist1 = Checkbar(root, ['01', 'O2', 'P7', 'P8'])
   elist2 = Checkbar(root, ['AF3', 'F7', 'F3', 'FC5'])
   elist3 = Checkbar(root, ['T7', 'T8', 'FC6', 'F4'])
   elist4 = Checkbar(root, ['F8', 'AF4', 'X', 'Y'])
   elist1.pack(side=TOP,  fill=X)
   elist2.pack()
   elist3.pack()
   elist4.pack()

   def allstates(): 
      fulllist = []
      fulllist.append(list(elist1.state()))
      fulllist.append(list(elist2.state()))
      fulllist.append(list(elist3.state()))
      fulllist.append(list(elist4.state()))
      print(fulllist)
   
   Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
   Button(root, text='Peek', command=allstates).pack(side=RIGHT)
   Button(root, text='Start', command=startplotting).pack(side=RIGHT)
   root.mainloop()

#O1 O2 P7 P8 AF3 F7 F3 FC5 T7 T8 FC6 F4 F8 AF4 X Y