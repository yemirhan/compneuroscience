# -*- coding: utf-8 -*-
"""
@author: Christodoulos Benetatos - xribene
         Yusuf Emirhan Şahin - yemirhan
"""
###############################################################################
from __future__ import division
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from emokit.emotiv import Emotiv
import matplotlib.pyplot as plt
from collections import deque
from scipy import signal,fft
from Queue import Queue
import time, threading
import numpy as np
import sys
import os
import datetime
###############################################################################
# Helper functions

def eeg_fft(y,Fs=128,show=False,limits=[0,30,0,20]) : 
    y=np.atleast_2d(y)
    [C,N]=np.shape(y)
    T=1/Fs
    y_f = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2,endpoint=False)
    xf=np.atleast_2d(xf)
    xf=np.tile(xf,(C,1))
    yf= (np.square(2.0/N *np.abs(y_f[:,0:N//2])))
    if show:
        plt.ion()
        plt.plot(np.squeeze(xf), np.squeeze(yf))
        plt.axis(limits)
        plt.xticks(range(limits[1]))
        plt.grid()
    return yf,xf

def filtering(eeg,cut_off=[2,40],mode='band',order=4,show=False,limits=[0,30,0,20],ex=[111,111]):
    eeg=np.atleast_2d(eeg)
    [C,N]=np.shape(eeg)
    tmp=np.zeros(shape=(np.shape(eeg)))
    b, a = signal.butter(order, np.array((cut_off))/(Fs/2), btype = mode)
    for i in xrange(C):
        if (i==ex[0]) or (i==ex[1]):
            tmp[i,:]=eeg[i,:]
            continue
        tmp[i,:]=signal.filtfilt(b, a, eeg[i,:] ) 
        #print np.mean(tmp[i,:])
    if show:
        eeg_fft(np.squeeze(eeg),Fs,show,limits)
        eeg_fft(np.squeeze(tmp),Fs,show,limits)
    return tmp

def quality_color(av):
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

print "Success!"
##############################################################################
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

class Plotter(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
# reads data from emotiv and sends them to Plotter every 'step/Fs' seconds,
# through q1
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
                        data=''
                        for name in electrodes.split(' '):
                            data = str(data) + str(packet.sensors[name]['value']) + ' ' + str(packet.sensors[name]['quality']) + ' '
                        O1_buff.write(data) 
                        #writeData(data)#cogs lab addition
                        if (writetime == 1):
                            file.write(str(data)+ " :   " + str(datetime.datetime.utcnow()) + "\n")#adds time
                        else: 
                            file.write(str(data)+ "\n")#cogs lab addition
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


##############################################################################
if __name__ == '__main__':
    Fs=128
    # O1 O2 P7 P8 AF3 F7 F3 FC5 T7 T8 FC6 F4 F8 AF4 X Y
    electrodes='O1 O2 P7 P8 AF3 F7 F3 FC5 T7 T8 FC6 F4 F8 AF4 X Y' # choose which sensors to graph
    tw_sec=2 # time window in which fft will be calculated 
    q1=Queue()
    step=np.round(0.5*Fs) # how many new points will be graphed in every update
    # or how many seconds (0.5) between update_plots repetetions
    # or overlap between tw_sec windows
    flag1=threading.Event()
    writetime = input("1: write time, 0: do not write time : ")
    #while ("MATLAB.exe" not in (os.popen("tasklist /fi \"windowtitle eq PTB*\"").read())):
    #    pass
    file = open("myData.txt", 'w')
    thread1=Reader(q1,flag1,step,tw_sec,electrodes)
    show=1
    app = QtGui.QApplication(sys.argv)
    s = Plotter()
    #writeData(q1) #cogs lab addition
    thread1.start()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_() 
    thread1.stop()
