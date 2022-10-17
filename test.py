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

class processLifecycle(QObject):

    def controlCycles(self):
        global cycleCount
        global fileCommands

        thisProcess= str(QThread.currentThread()).split(") at ",1)[1].replace('>', '')

        np.random.seed()

        self.newCycle(thisProcess)
        self.readyCycle(thisProcess)
        readFile()

        for command in fileCommands:
            if command[0].lower() == 'calculate':
                self.runCycle(int(command[1]), int(command[2]), thisProcess)
            elif command[0].lower() == 'i/o':
                self.waitCycle(int(command[1]), int(command[2]), thisProcess)
        self.exitCycle(thisProcess)

    def newCycle(self, process):
        global cycleCount
        global saveLog
        window.updateTextbox("Loading process " + process)
        saveLog+=("Loading process " + process + "\n")
        start = time.perf_counter()
        for i in range(np.random.randint(5,15)):
            cycleCount+=1
            window.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
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
            window.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
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
            window.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
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
            window.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
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
            window.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycleCount), None))
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
        self.thread1 = QThread()
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker1 = processLifecycle()
        self.worker2 = processLifecycle()
        # Step 4: Move worker to the thread
        self.worker1.moveToThread(self.thread1)
        self.worker2.moveToThread(self.thread2)
        # Step 5: Connect signals and slots
        self.thread1.started.connect(self.worker1.controlCycles)
        self.thread2.started.connect(self.worker2.controlCycles)
        # Step 6: Start the thread
        self.thread1.start()
        self.thread2.start()
    
    def updateScreen(self, cycle, process, cpu, memory, disk):
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycle), None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Process Count: " + str(process), None))
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", u"CPU: " + str(cpu) + '%', None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", u"Memory: " + str(memory) + ' MB', None))
    
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