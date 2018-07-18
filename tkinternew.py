from Tkinter import *
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

def create_window():
    buttonwindow = Toplevel(root)
    

if __name__ == '__main__':
    electrodes = ''
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
        create_window()
    b = Button(root, text="Start", command=allstates)
    b.pack(fill=X)

    root.mainloop()