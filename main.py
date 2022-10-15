# Justin Hoyle
# Operating System Simulator w/ User Interface
# Main app file to run gui
# CMSC 312

from cProfile import run
from hashlib import new
from logging.config import stopListening
from platform import machine
import simpy
import sys
import random
import statistics
import os, psutil

from ui_cmsc312 import Ui_MainWindow

from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import (QCoreApplication)

wait_times = []
currentProcessCount = 0
currentCycleCount = 0

# Change to toal count
newLCount = 0
readyLCount = 0
runLCount = 0
waitLCount = 0
exitLCount = 0

# Get CPU % and memory in MBs
print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
print(psutil.Process(os.getpid()).cpu_times())

class Factory(object):
    def __init__(self, env, assemblyCount, computerCount, testFieldCount):
        self.env = env
        self.assemblyMachine = simpy.Resource(env, assemblyCount)
        self.computer = simpy.Resource(env, computerCount)
        self.testField = simpy.Resource(env, testFieldCount)

    # CALCULATE

    # Calculate random time it takes for a factory to assemble a droid from the given machine parts
    def assembleDroid(self, machinePart):
        window.updateRun(1)
        window.updateTextbox("Assembling droid #" + str(machinePart) + "...")
        yield self.env.timeout(random.randint(1, 5))
        window.updateRun(-1)

    # Calculate time it takes for a factory to program a droid from the given machine parts
    def programOrders(self, machineParts):
        window.updateRun(1)
        window.updateTextbox("Programming droid #" + str(machineParts) + "...")
        yield self.env.timeout(5)
        window.updateRun(-1)

    # Calculate random time it takes for a factory to test an assembled droid from the given machine parts
    def testDroid(self, machineParts):
        window.updateRun(1)
        window.updateTextbox("Testing droid #" + str(machineParts) + "...")
        yield self.env.timeout(random.randint(1, 10)) 
        window.updateRun(-1) 


def createDroid(env, machineParts, factory):
    global currentProcessCount
    currentProcessCount = 1+currentProcessCount
    window.updateTextbox("Starting process " + str(machineParts) + "...")
    arrival_time = env.now

    # I/O
    
    # Wait for assembly machine to finish previous request
    with factory.assemblyMachine.request() as request:
        yield request
        yield env.process(factory.assembleDroid(machineParts))
    
    # Wait for computer to finish previous request
    with factory.computer.request() as request:
        yield request
        yield env.process(factory.programOrders(machineParts))
    
    # Wait for test field to finish previous request
    with factory.testField.request() as request:
        yield request     
        yield env.process(factory.testDroid(machineParts))
 
    # Machine parts arrive in factory
    wait_times.append(env.now - arrival_time)


def startFactory(env, assemblyCount, computerCount, testFieldCount):
    factory = Factory(env, assemblyCount, computerCount, testFieldCount)
    window.updateTextbox("Starting factory...")
    # FORK

    for machinePart in range(3):
        window.updateNew(1)
        env.process(createDroid(env, machinePart, factory))
        window.updateExit(1)
        window.updateExit(-1)
        window.updateNew(-1)

    while True:
        window.updateWait(1)
        yield env.timeout(0.20)
        window.updateWait(-1)
        window.updateNew(1)
        machinePart += 1
        env.process(createDroid(env, machinePart, factory))
        window.updateExit(1)
        window.updateExit(-1)
        window.updateNew(-1)
    


def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def get_user_input():
    num_assembly = input("Input # of assembly machines working: ")
    num_program = input("Input # of programming machines working: ")
    num_field = input("Input # of test fields working: ")
    params = [num_assembly, num_program, num_field]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. Simulation will use default values:",
            "\n1 assembly machine, 1 programming machine, 1 test field.",
        )
        params = [1, 1, 1]
    return params


def main():
    # Setup
    random.seed(42)
    num_assembly, num_program, num_field = get_user_input()

    # Run the simulation
    env = simpy.Environment()
    env.process(startFactory(env, num_assembly, num_program, num_field))
    env.run(until=90) # SImulate running for 90 minutes
    window.updateWait(-1)
    window.updateRun(-runLCount)

    # View the results
    mins, secs = get_average_wait_time(wait_times)
    text = "Stopping simulation..." + f"\nThe average run time is {mins} minutes and {secs} seconds."
    window.updateTextbox(text)
    print(f"The average run time is {mins} minutes and {secs} seconds.",)

    
# Launch GUI
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #Initialize gui
        QMainWindow.__init__(self)
        self.setupUi(self)
    
    def updateScreen(self, cycle, process, cpu, memory, disk):
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count: " + str(cycle), None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Processes Count: " + str(process), None))
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


# Run Program
if __name__ == "__main__":
    #main()
    app = QApplication(sys.argv)
    window = Main()
    main()
    window.show()
    window.updateScreen(0,0,0,0,0)
    sys.exit(app.exec())