from PyQt5.QtWidgets import *
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()


        self.setGeometry(50,0,1024,576)
        self.setWindowTitle("Real Time Peak")
        self.show()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())