from PyQt5.QtWidgets import * 
import sys

class Window(QWidget): 
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.o1 = QCheckBox("O1")
        self.o1.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.o1, 0, 0)
        self.o2 = QCheckBox("O2")
        self.o2.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.o2, 0, 1)
        self.p7 = QCheckBox("P7")
        self.p7.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.p7, 0, 2)
        self.p8 = QCheckBox("P8")
        self.p8.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.p8, 0, 3)
        self.af3 = QCheckBox("AF3")
        self.af3.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.af3, 1, 0)
        self.f7 = QCheckBox("F7")
        self.f7.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.f7, 1, 1)
        self.f3 = QCheckBox("F3")
        self.f3.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.f3, 1, 2)
        self.fc5 = QCheckBox("FC5")
        self.fc5.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.fc5, 1, 3)
        self.t7 = QCheckBox("T7")
        self.t7.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.t7, 2, 0)
        self.t8 = QCheckBox("T8")
        self.t8.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.t8, 2, 1)
        self.fc6 = QCheckBox("FC6")
        self.fc6.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.fc6, 2, 2)
        self.f4 = QCheckBox("F4")
        self.f4.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.f4, 2, 3)
        self.f8 = QCheckBox("F8")
        self.f8.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.f8, 3, 0)
        self.af4 = QCheckBox("AF4")
        self.af4.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.af4, 3, 1)
        self.x = QCheckBox("X")
        self.x.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.x, 3, 2)
        self.y = QCheckBox("Y")
        self.y.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.y, 3, 3)

        button = QPushButton("Kaydet")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button, 4, 1, 1, 2)


    def checkbox_toggled(self):
        selectlist = [0, 0, 0]
        if self.o1.isChecked(): 
            selectlist[0] = 1
        if self.o2.isChecked(): 
            selectlist[1] = 1
        if self.p7.isChecked(): 
            selectlist[2] = 1
        selectlist1 = selectlist
        print(selectlist1)
    def on_button_clicked(self): 
        print("The button was pressed!")


if __name__ == "__main__":
    electrodelist = ['O1', 'O2', 'P7', 'P8', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'T8', 'FC6', 'F4', 'F8', 'AF4', 'X', 'Y']
    selectlist1 = [0, 0, 0] 
    electrodes = ''
    
    app = QApplication(sys.argv)

    screen = Window()
    screen.show()
    print(electrodes + "\n")
    for i in range(len(selectlist1)):
        if i is 1:
            electrodes = electrodes + str(electrodelist[i]) + " "
