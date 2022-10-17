# Justin Hoyle
# Operating System Simulator w/ User Interface
# Main app file to run gui
# CMSC 312

# TODO Add file loading system/worker count
# Start, stop, pause
# FIND OUT HOW TO PAUSE
# Check if load file exists

from ast import arg
from cProfile import run
from hashlib import new
from logging.config import stopListening
from platform import machine
import simpy
import sys
import random
import statistics
import os, psutil
import random
import string
import time
import multiprocessing as mp
from ctypes import c_int
from multiprocessing import Value, Lock, Process
import numpy as np


from ui_cmsc312 import Ui_MainWindow

from PySide6.QtWidgets import (QApplication, QMainWindow, QInputDialog)
from PySide6.QtCore import (QCoreApplication, QObject, QThread)
from PySide6 import QtTest


saveLog = ''
wait_times = []
currentProcessCount = 0
currentCycleCount = 0

# Change to toal count
newLCount = 0
readyLCount = 0
runLCount = 0
waitLCount = 0
exitLCount = 0

cycleCount = 0

fileCommands = []
fileName = ''

# Get CPU % and memory in MBs
#print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
#print(psutil.Process(os.getpid()).cpu_times())

def readFile():
    global fileCommands
    global fileName
    fileCommands = [line.strip().split(',') for line in open(fileName)]

def writeFile():
    global saveLog
    text_file = open("Simulator Log.txt", "w")
    text_file.write(saveLog)
    text_file.close()

class threadCounter():
    def __init__(self):
        self._counter = [0,0,0,0,0]
        # initialize lock
        self._lock = Lock()
    
    def increment(self, i):
        with self._lock:
            self._counter[i] += 1
    
    def value(self, i):
        with self._lock:
            return self._counter[i]

class processLifecycle(QObject):

    def controlCycles(self, counter):
        global cycleCount
        global fileCommands

        thisProcess= str(QThread.currentThread()).split(") at ",1)[1].replace('>', '')

        np.random.seed()

        self.newCycle(thisProcess, counter)
        self.readyCycle(thisProcess)
        readFile()

        for command in fileCommands:
            if command[0].lower() == 'calculate':
                self.runCycle(int(command[1]), int(command[2]), thisProcess)
            elif command[0].lower() == 'i/o':
                self.waitCycle(int(command[1]), int(command[2]), thisProcess)
        self.exitCycle(thisProcess)

    def newCycle(self, process, counter):
        global cycleCount
        global saveLog
        window.updateTextbox("Loading process " + process)
        saveLog+=("Loading process " + process + "\n")
        counter.increment(0)
        print(counter.value(0))
        start = time.perf_counter()
        for i in range(np.random.randint(5,15)):
            cycleCount+=1
            window.updateScreen(counter.value(0),counter.value(1),counter.value(2),counter.value(3),counter.value(4))
            QtTest.QTest.qWait(250)  
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" loading finished in {stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" loading finished in {stop - start:0.2f} seconds\n")

    def readyCycle(self, process):
        global cycleCount
        global saveLog
        window.updateTextbox("Process " + process + " is ready to run")
        saveLog+=("Process " + process + " is ready to run\n")
        start = time.perf_counter()
        for i in range(np.random.randint(5,15)):
            cycleCount+=1
            window.updateScreen()
            QtTest.QTest.qWait(250)       
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" in ready state {stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" in ready state {stop - start:0.2f} seconds\n")

    def runCycle(self, min, max, process):
        global cycleCount
        global saveLog
        window.updateTextbox("Running calculation for process " + process)
        saveLog+=("Running calculation for process " + process + "\n")
        start = time.perf_counter()
        for i in range(np.random.randint(min, max)):
            cycleCount+=1
            window.updateScreen()
            QtTest.QTest.qWait(250)
        stop = time.perf_counter()
        window.updateTextbox("Process " + process + f" ran in {stop - start:0.2f} seconds")
        saveLog+=("Process " + process + f" ran in {stop - start:0.2f} seconds\n")


    def waitCycle(self, min, max, process):
        global cycleCount
        global saveLog
        window.updateTextbox("Waiting on I/O completion for process " + process)
        saveLog+=("Waiting on I/O completion for process " + process + "\n")
        start = time.perf_counter()
        for i in range(np.random.randint(min, max)):
            cycleCount+=1
            window.updateScreen()
            QtTest.QTest.qWait(250)
        stop = time.perf_counter()
        window.updateTextbox(f"Process " + process + f" halted for {stop - start:0.2f} seconds")
        saveLog+=(f"Process " + process + f" halted for {stop - start:0.2f} seconds\n")


    def exitCycle(self, process):
        global cycleCount
        global saveLog
        window.updateTextbox("Process " + process + " complete, releasing resources")
        saveLog+=("Process " + process + " complete, releasing resources\n")
        start = time.perf_counter()
        for i in range(np.random.randint(5,15)):
            cycleCount+=1
            window.updateScreen()
            QtTest.QTest.qWait(250)
        stop = time.perf_counter()
        window.updateTextbox("Exit for process " + process + f" finished in {stop - start:0.2f} seconds")
        saveLog+=("Exit for process " + process + f" finished in {stop - start:0.2f} seconds\n")

def startProcess():
    global currentProcessCount
    currentProcessCount = 1+currentProcessCount
    window.updateTextbox("Starting process " + str(currentProcessCount) + "...")
    e = mp.Event()
    start = mp.Event()

    processObj = [processLifecycle() for i in range(2)]
    #processLifecycle().controlCycles()
    
    with mp.Pool(processes=4) as pool:                                                                                           
            pool.map(processLifecycle.controlCycles, processObj)
    
# Launch GUI
class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        #Initialize gui
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.startButton.clicked.connect(self.startClicked)
        self.loadButton.clicked.connect(self.getFile)
        self.saveLogButton.clicked.connect(self.writeFile)
    
    def startClicked(self):
        self.runLongTask()
    
    def getFile(self):
        global fileName
        text, ok = QInputDialog.getText(self, 'Load File', 'Enter file name:')
		
        if ok:
            self.fileLoadedLabel.setText('File Loaded: ' + str(text))
            fileName = text

    def writeFile(self):
        writeFile()
    
    def runLongTask(self):
        # Step 2: Create a QThread object
        counter = threadCounter()
        self.threads = [QThread() for i in range(2)]
        #self.thread1 = QThread()
        #self.thread2 = QThread()
        # Step 3: Create a worker object
        self.workers = [processLifecycle() for thread in self.threads]
        #self.worker1 = processLifecycle()
        #self.worker2 = processLifecycle()
        # Step 4: Move worker to the thread
        for worker, thread in zip(self.workers, self.threads):
            worker.moveToThread(thread)
        #self.worker1.moveToThread(self.thread1)
        #self.worker2.moveToThread(self.thread2)
        # Step 5: Connect signals and slots
        for worker, thread in zip(self.workers, self.threads):
            thread.started.connect(worker.controlCycles(counter))
        #self.thread1.started.connect(self.worker1.controlCycles)
        #self.thread2.started.connect(self.worker2.controlCycles)
        # Step 6: Start the thread
        for thread in self.threads:
            thread.start()
        
        #for thread in self.threads:
            #thread.join()
        #self.thread1.start()
        #self.thread2.start()
    
    
    def updateScreen(self, new, ready, run, wait, exitV):
        global cycleCount

        self.newLabel.setText(QCoreApplication.translate("MainWindow", u"New: " + str(new), None))
        self.readyLabel.setText(QCoreApplication.translate("MainWindow", u"Ready: " + str(ready), None))
        self.runLabel.setText(QCoreApplication.translate("MainWindow", u"Run: " + str(run), None))
        self.waitLabel.setText(QCoreApplication.translate("MainWindow", u"Wait: " + str(wait), None))
        self.exitLabel.setText(QCoreApplication.translate("MainWindow", u"Exit: " + str(exitV), None))
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Process Count: " + str(2), None))
        # CPU % will likely always be zero due to how python is not closely related to the cpu
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", f"CPU: {psutil.Process(os.getpid()).cpu_percent():0.2f}%", None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", f"Memory: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:0.2f} MB", None))
    
    def updateTextbox(self, text):
        self.proccessViewer.append(text)
    
    def updateNew(self, check):
        global newLCount
        newLCount = newLCount + check
        self.newLabel.setText(QCoreApplication.translate("MainWindow", u"New: " + str(newLCount), None))
    
    def updateReady(self, check):
        global readyLCount
        readyLCount = readyLCount + check
        self.readyLabel.setText(QCoreApplication.translate("MainWindow", u"Ready: " + str(readyLCount), None))
    
    def updateRun(self, check):
        global runLCount
        runLCount = runLCount + check
        self.runLabel.setText(QCoreApplication.translate("MainWindow", u"Run: " + str(runLCount), None))
    
    def updateWait(self, check):
        global waitLCount
        waitLCount = waitLCount + check
        self.waitLabel.setText(QCoreApplication.translate("MainWindow", u"Wait: " + str(waitLCount), None))
    
    def updateExit(self, check):
        global exitLCount
        exitLCount = exitLCount + check
        self.exitLabel.setText(QCoreApplication.translate("MainWindow", u"Exit: " + str(exitLCount), None))

app = QApplication(sys.argv)
window = Main()

# Run Program
if __name__ == "__main__":
    #main()
    window.show()
    window.updateScreen(0,0,0,0,0)
    #startProcess()
    sys.exit(app.exec())