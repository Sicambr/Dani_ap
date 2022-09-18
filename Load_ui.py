import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
#from PyQt5.QtCore import *
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('Firs_form.ui', self) # Load the .ui file
        #self.show() # Show the GUI

        #button = self.findChild(QPushButton, 'pushButton')
        #button.clicked.connect(self.clicked_btn)
        layout = QVBoxLayout()
        wdg = self.findChild(QWidget, 'scrollAreaWidgetContents')
        for n in range(20):
            button = QPushButton(str(n))
            layout.addWidget(button)
        wdg.setLayout(layout)


    def clicked_btn(self):
        print('Button clicked')


app = QApplication([])
window = UI()
window.show()
app.exec_()