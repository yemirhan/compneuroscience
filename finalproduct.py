################################
from __future__ import division
from Tkinter import *
from emokit.emotiv import Emotiv
from collections import deque
from scipy import signal, fft
from Queue import Queue
import numpy as np
import time
import threading
import sys
import os
import os.path
################################
#additional functions

def  quality_color(av):
    aa=av//20
    aa=(aa<255)*aa+(aa>255)*255+(aa==255)*255
    return (255-aa, aa, 0)
def pad(array_in, result):
    # zero pad array so that shape(array_in)=shape(result)
    [a,b]=np.shape(array_in)
    [k,l]=np.shape(result)
    start1=int((k-a)/2)
    start2=int((l-b)/2)
    result[start1:(start1+a),start2:(start2+b)]=array_in
    return result
def next_pow(x):
    return 1<<(x-1).bit_length()
def writeData(q1):
        #self.q1=q1
    filename = "myData.txt"

    file = open(filename, 'w')
    file.write('%d' % q1)
    file.close()

#####################


class ring_buffer(object):
    def __init__(self,size):
        self.size=size
        self._buffered= deque([], self.size)
    def write(self, value):
        self._buffered.append(value)
    def write_ex(self, value):
        self._buffered.extend(value)
    def show(self):
        print(self._buffered)
    def copy(self,overlap):
        tmp=list(self._buffered)
        return tmp[0:overlap]
    def calls(self):
        return self.write.calls
    def list_ret(self):
        a=list(self._buffered)
        return a


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
    elist2.pack(fill=X)
    elist3.pack(fill=X)
    elist4.pack(fill=X)
    def allstates(): 
        fulllist = []
        electrodes = ''
        electrodelist = ['01', 'O2', 'P7', 'P8', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'T8', 'FC6', 'F4', 'F8', 'AF4', 'X', 'Y']
        fulllist.append(list(elist1.state()))
        fulllist.append(list(elist2.state()))
        fulllist.append(list(elist3.state()))
        fulllist.append(list(elist4.state()))
        print(fulllist)
        for i in range(4):
            for j in range(4):
                if fulllist[i][j] is 1:
                    electrodes = electrodes + str(electrodelist[i*4 + j]) + " "
        print(electrodes)
        Fs = 128
        tw_sec = 2  # time window in which fft will be calculated
        q1 = Queue()
        step = np.round(0.5*Fs)  # how many points will be graphed in every updt
        # or how many seconds (0.5) between update_plots repetetions
        # or overlap between tw_sec windows
        flag1 = threading.Event()
        thread1 = Reader(q1, flag1, step, tw_sec, electrodes)
        thread1.start()
        buttonwindow = Toplevel(root)
        Button(buttonwindow, text='Quit', command=root.quit).pack(side=RIGHT)
        buttonwindow.pack()
        buttonwindow.mainloop()
        thread1.stop()
    b = Button(root, text="Start", command=allstates)
    b.pack(fill=X)

    root.mainloop()
    