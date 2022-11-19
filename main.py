# Justin Hoyle
# Operating System Simulator w/ User Interface
# Main app file to run gui
# CMSC 312

# Be sure to create .exe file justin

# TEMPLATE FOR TEXT INPUT FILE
######################################
# Commands must be listed as command(Calculate,I/O),min(int),max(int)
######################################
# Operation List,Min Cycles,Max Cycles
# Calculate,5,100
# Calculate,25,50
# I/O,10,20
# Calculate,5,20
# I/O,15,25

import sys, os, psutil, time, numpy as np
from multiprocessing import Lock

from ui_cmsc312 import Ui_MainWindow

from PySide6.QtWidgets import (QApplication, QMainWindow, QInputDialog, QMessageBox)
from PySide6.QtCore import (QCoreApplication, QObject, QThread)
from PySide6 import QtTest

# Declare global vars
saveLog = ''
processCount = 0
cycleCount = 0
cycleLimit = 0
fileCommands = []
fileName = ''
pause = False
resumeFromCycleCount = False

# Read input file
def readFile():
    global fileCommands
    global fileName
    fileCommands = [line.strip().split(',') for line in open(fileName)]

# Create log file
def writeFile():
    global saveLog
    text_file = open("Simulator Log.txt", "w")
    text_file.write(saveLog)
    text_file.close()

# Count current states of threads and cycle count
class threadCounter():
    def __init__(self):
        # New, ready, run, wait, and exit process count, Cycle count, and 'current memory size'
        self._counter = [0,0,0,0,0,0,0]
        # initialize lock
        self._lock = Lock()
    
    def incrementMem(self, mem):
        with self._lock:
            self._counter[6] += mem
    
    def deincrementMem(self, mem):
        with self._lock:
            self._counter[6] -= mem

    def increment(self, i):
        with self._lock:
            self._counter[i] += 1
    
    def deincrement(self, i):
        with self._lock:
            self._counter[i] -= 1
    
    def value(self, i):
        with self._lock:
            return self._counter[i]

# Pause threads at set cycle count
class processLifecycle(QObject):

    def __init__(self, counter):
        super(processLifecycle, self).__init__()
        self.counter = counter

    # Check cycle count and puase if met
    def checkCycleCount(self):
        global pause
        global resumeFromCycleCount
        global cycleLimit

        if not resumeFromCycleCount and self.counter.value(5) == int(cycleLimit) and int(cycleLimit) != 0:
            pause = True
            resumeFromCycleCount = True

    def controlCycles(self):
        global fileCommands

        # get thread address
        thisProcess= str(QThread.currentThread()).split(") at ",1)[1].replace('>', '')

        # Generate random seeds for each thread
        np.random.seed()

        # Start new cycle and then put in to ready state
        allocMem = self.newCycle(thisProcess)
        self.readyCycle(thisProcess)
        readFile()

        # Read commands to determine calculate, or wait
        for command in fileCommands:
            if command[0].lower() == 'calculate':
                self.runCycle(int(command[1]), int(command[2]), thisProcess)
            elif command[0].lower() == 'i/o':
                self.waitCycle(int(command[1]), int(command[2]), thisProcess)
        # Start exit
        self.exitCycle(thisProcess, allocMem)

    # Run new lifecycle
    def newCycle(self, process):
        global saveLog
        global pause
        # "Allocate" memory for new process of random size from 50 to 150
        allocMem = np.random.randint(50,150)
        self.counter.incrementMem(allocMem)

        # Check if there is space to exit the new cycle state, halt if not
        while self.counter.value(6) > 512:
            QtTest.QTest.qWait(10)

        window.updateTextbox("Loading process " + process)
        saveLog+=("Loading process " + process + "\n")
        self.counter.increment(0)
        start = time.perf_counter()
        pauseTime = 0
        for i in range(np.random.randint(5,15)):
            self.checkCycleCount()
            if not pause:
                self.counter.increment(5)
                window.updateScreen(self.counter.value(0),self.counter.value(1),self.counter.value(2),self.counter.value(3),self.counter.value(4),self.counter.value(5),self.counter.value(6))
                QtTest.QTest.qWait(250)  
            else:
                pauseTime += time.perf_counter() - start
                while pause:
                    QtTest.QTest.qWait(10)
                start = time.perf_counter()
                
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" loading finished in {pauseTime + stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" loading finished in {stop - start:0.2f} seconds\n")
        self.counter.deincrement(0)
        return allocMem

    # Run ready lifecycle
    def readyCycle(self, process):
        global saveLog
        window.updateTextbox("Process " + process + " is ready to run")
        saveLog+=("Process " + process + " is ready to run\n")
        self.counter.increment(1)
        start = time.perf_counter()
        pauseTime = 0
        for i in range(np.random.randint(5,15)):
            self.checkCycleCount()
            if not pause:
                self.counter.increment(5)
                window.updateScreen(self.counter.value(0),self.counter.value(1),self.counter.value(2),self.counter.value(3),self.counter.value(4),self.counter.value(5),self.counter.value(6))
                QtTest.QTest.qWait(250)  
            else:
                pauseTime += time.perf_counter() - start
                while pause:
                    QtTest.QTest.qWait(10)
                start = time.perf_counter()    
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" in ready state {pauseTime + stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" in ready state {stop - start:0.2f} seconds\n")
        self.counter.deincrement(1)

    # Run calculate, 'run' lifecycle
    def runCycle(self, min, max, process):
        global saveLog
        window.updateTextbox("Running calculation for process " + process)
        saveLog+=("Running calculation for process " + process + "\n")
        self.counter.increment(2)
        start = time.perf_counter()
        pauseTime = 0
        for i in range(np.random.randint(min,max)):
            self.checkCycleCount()
            if not pause:
                self.counter.increment(5)
                window.updateScreen(self.counter.value(0),self.counter.value(1),self.counter.value(2),self.counter.value(3),self.counter.value(4),self.counter.value(5),self.counter.value(6))
                QtTest.QTest.qWait(250)  
            else:
                pauseTime += time.perf_counter() - start
                while pause:
                    QtTest.QTest.qWait(10)
                start = time.perf_counter()
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" ran in {stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" ran in {stop - start:0.2f} seconds\n")
        self.counter.deincrement(2)


    # Run wait, I/O lifecycle
    def waitCycle(self, min, max, process):
        global saveLog
        window.updateTextbox("Waiting on I/O completion for process " + process)
        saveLog+=("Waiting on I/O completion for process " + process + "\n")
        self.counter.increment(3)
        start = time.perf_counter()
        pauseTime = 0
        for i in range(np.random.randint(min,max)):
            self.checkCycleCount()
            if not pause:
                self.counter.increment(5)
                window.updateScreen(self.counter.value(0),self.counter.value(1),self.counter.value(2),self.counter.value(3),self.counter.value(4),self.counter.value(5),self.counter.value(6))
                QtTest.QTest.qWait(250)  
            else:
                pauseTime += time.perf_counter() - start
                while pause:
                    QtTest.QTest.qWait(10)
                start = time.perf_counter()
        stop = time.perf_counter()
        window.updateTextbox(f"Process " + process + f" halted for {stop - start:0.2f} seconds")
        saveLog+=(f"Process " + process + f" halted for {stop - start:0.2f} seconds\n")
        self.counter.deincrement(3)


    # Run exit lifecycle
    def exitCycle(self, process, allocMem):
        global saveLog
        window.updateTextbox("Process " + process + " complete, releasing resources")
        saveLog+=("Process " + process + " complete, releasing resources\n")
        self.counter.increment(4)
        start = time.perf_counter()
        pauseTime = 0
        for i in range(np.random.randint(5,15)):
            self.checkCycleCount()
            if not pause:
                self.counter.increment(5)
                window.updateScreen(self.counter.value(0),self.counter.value(1),self.counter.value(2),self.counter.value(3),self.counter.value(4),self.counter.value(5),self.counter.value(6))
                QtTest.QTest.qWait(250)  
            else:
                pauseTime += time.perf_counter() - start
                while pause:
                    QtTest.QTest.qWait(10)
                start = time.perf_counter()
        stop = time.perf_counter()
        self.counter.deincrement(4)
        self.counter.deincrementMem(allocMem)
        window.updateTextbox("Exit for process " + process + f" finished in {stop - start:0.2f} seconds")
        saveLog+=("Exit for process " + process + f" finished in {stop - start:0.2f} seconds\n")
    
# GUI class
class Main(QMainWindow, Ui_MainWindow):

    #Initialize gui
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.startButton.clicked.connect(self.startClicked)
        self.loadButton.clicked.connect(self.getFile)
        self.saveLogButton.clicked.connect(self.writeFile)
        self.pauseButton.clicked.connect(self.pause)
        self.resumeButton.clicked.connect(self.resume)
        self.setCycleButton.clicked.connect(self.setCycleLimit)
    
    # Link button to start simulation
    def startClicked(self):
        global fileName
        if fileName:
            self.runLongTask()
        else:
            popup = QMessageBox(QMessageBox.Critical,"File load error","No file loaded!",QMessageBox.Ok,self)
            popup.show()

    # Ask for file name input and make sure it exists, then ask for desired number of threads
    def getFile(self, invalid):
        global fileName
        global processCount

        if not invalid:
            text, ok = QInputDialog.getText(self, 'Load File', 'Enter file name:')
		
            if ok:
                if os.path.exists(str(text)):
                    self.fileLoadedLabel.setText('File Loaded: ' + str(text))
                    fileName = text
                    text, ok = QInputDialog.getText(self, 'Process Count', 'Enter number of processes:')
                    processCount = int(text)
                else:
                    self.getFile(True)
        
        else:
            text, ok = QInputDialog.getText(self, 'Load File', ' INVALID FILE NAME - Enter file name:')

            if ok:
                if os.path.exists(str(text)):
                    self.fileLoadedLabel.setText('File Loaded: ' + str(text))
                    fileName = text
                    text, ok = QInputDialog.getText(self, 'Process Count', 'Enter number of processes:')
                    processCount = int(text)
                else:
                    self.getFile(True)

    # Create log file
    def writeFile(self):
        writeFile()
    
    # Set cycle limit
    def setCycleLimit(self):
        global cycleLimit   
        cycleLimit = self.cycleCountInput.text()
    
    # Start simulation
    def runLongTask(self):
        global processCount
        counter = threadCounter()

        # Create a QThread object    
        self.threads = [QThread() for i in range(processCount)]

        # Create a worker object
        self.workers = [processLifecycle(counter) for thread in self.threads]

        # Move worker to the thread
        for worker, thread in zip(self.workers, self.threads):
            worker.moveToThread(thread)

        # Connect signals and slots
        for worker, thread in zip(self.workers, self.threads):
            thread.started.connect(worker.controlCycles)

        # Start the thread
        for thread in self.threads:
            thread.start()   
    
    # Pause thread
    def pause(self):
        global pause
        pause = True
    
    # Resume thread
    def resume(self):
        global pause
        pause = False

    # Update resources/process states
    def updateScreen(self, new, ready, run, wait, exitV, counter, extraMem):
        global processCount
        self.newLabel.setText(QCoreApplication.translate("MainWindow", u"New: " + str(new), None))
        self.readyLabel.setText(QCoreApplication.translate("MainWindow", u"Ready: " + str(ready), None))
        self.runLabel.setText(QCoreApplication.translate("MainWindow", u"Run: " + str(run), None))
        self.waitLabel.setText(QCoreApplication.translate("MainWindow", u"Wait: " + str(wait), None))
        self.exitLabel.setText(QCoreApplication.translate("MainWindow", u"Exit: " + str(exitV), None))
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(counter), None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Process Count: " + str(processCount), None))
        # CPU % will likely always be zero due to how python is not closely related to the cpu
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", f"CPU: {psutil.Process(os.getpid()).cpu_percent():0.2f}%", None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", f"Memory: {(extraMem+(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)):0.2f} MB", None))
        # >> 20 for MB
        #print(psutil.Process(os.getpid()).memory_info().vms)
    
    # Update main console
    def updateTextbox(self, text):
        self.proccessViewer.append(text)

# Initialize main window
app = QApplication(sys.argv)
window = Main()

# Run Program
if __name__ == "__main__":
    window.show()
    window.updateScreen(0,0,0,0,0,0,0)
    sys.exit(app.exec())