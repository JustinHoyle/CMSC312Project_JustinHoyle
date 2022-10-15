# Justin Hoyle
# Operating System Simulator w/ User Interface
# Main app file to run gui
# CMSC 312

import simpy
import sys
import random
import statistics
import os, psutil

from ui_cmsc312 import Ui_MainWindow

from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import (QCoreApplication)

wait_times = []

print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
print(psutil.Process(os.getpid()).cpu_percent())

class Factory(object):
    def __init__(self, env, assemblyCount, computerCount, testFieldCount):
        self.env = env
        self.assemblyMachine = simpy.Resource(env, assemblyCount)
        self.computer = simpy.Resource(env, computerCount)
        self.testField = simpy.Resource(env, testFieldCount)

    # CALCULATE

    # Calculate random time it takes for a factory to assemble a droid from the given machine parts
    def assembleDroid(self, machinePart):
        yield self.env.timeout(random.randint(1, 5))

    # Calculate time it takes for a factory to program a droid from the given machine parts
    def programOrders(self, machineParts):
        yield self.env.timeout(5)

    # Calculate random time it takes for a factory to test an assembled droid from the given machine parts
    def testDroid(self, machineParts):
        yield self.env.timeout(random.randint(1, 10))  


def createDroid(env, machineParts, factory):
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

    # FORK
    
    for machinePart in range(3):
        env.process(createDroid(env, machinePart, factory))

    while True:
        yield env.timeout(0.20)

        machinePart += 1
        env.process(createDroid(env, machinePart, factory))


def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def get_user_input():
    num_cashiers = input("Input # of cashiers working: ")
    num_servers = input("Input # of servers working: ")
    num_ushers = input("Input # of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. Simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher.",
        )
        params = [1, 1, 1]
    return params


def main():
    # Setup
    random.seed(42)
    num_cashiers, num_servers, num_ushers = get_user_input()

    # Run the simulation
    env = simpy.Environment()
    env.process(startFactory(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)

    # View the results
    mins, secs = get_average_wait_time(wait_times)
    print(
        "Running simulation...",
        f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )

    
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
        self.diskUse.setText(QCoreApplication.translate("MainWindow", u"Disk: " + str(disk) + ' MB/s', None))

# Run Program
if __name__ == "__main__":
    main()
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    window.updateScreen(0,0,0,0,0)
    sys.exit(app.exec())