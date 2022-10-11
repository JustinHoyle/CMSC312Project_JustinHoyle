# Justin Hoyle
# Operating System Simulator w/ User Interface
# Main app file to run gui
# CMSC 312

import sys

from ui_cmsc312 import Ui_MainWindow

from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import (QCoreApplication)

# Launch GUI
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
    
    def updateScreen(self, cycle, process, cpu, memory, disk):
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycle), None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Processes Count: " + str(process), None))
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", u"CPU: " + str(cpu) + '%', None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", u"Memory: " + str(memory) + ' MB', None))
        self.diskUse.setText(QCoreApplication.translate("MainWindow", u"Disk: " + str(disk) + ' MB/s', None))

# Run Program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    window.updateScreen(0,0,0,0,0)
    sys.exit(app.exec())