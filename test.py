"""Companion code to https://realpython.com/simulation-with-simpy/

'Simulating Real-World Processes With SimPy'

Python version: 3.7.3
SimPy version: 3.0.11
"""

import simpy
import random
import statistics

wait_times = []


class Factory(object):
    def __init__(self, env, assemblyCount, computerCount, testFieldCount):
        self.env = env
        self.assemblyMachine = simpy.Resource(env, assemblyCount)
        self.computer = simpy.Resource(env, computerCount)
        self.testField = simpy.Resource(env, testFieldCount)

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

    # Moviegoer heads into the theater
    wait_times.append(env.now - arrival_time)


def startFactory(env, assemblyCount, computerCount, testFieldCount):
    factory = Factory(env, assemblyCount, computerCount, testFieldCount)

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


if __name__ == "__main__":
    main()
