import sys

from PyQt5.QtWidgets import QApplication 

from MainWindow import MainWindow
from Glovox import Glovox

qdark_present = True
try:
    import qdarkstyle  
except ImportError:
    qdark_present = False

if __name__ == '__main__':

    app = QApplication(sys.argv)

	#The Model
    model = Glovox() 

    if qdark_present:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    #The View/Controller
    window = MainWindow(model) 
    sys.exit(app.exec_())