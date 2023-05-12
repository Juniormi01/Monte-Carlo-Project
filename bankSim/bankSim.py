# bankSim.py
# Bank-Queue-Simulation
# CSCI 154

# The following program simulates a bank queue.
   
# Logic:
#
#   While (there is a Teller in the Teller Line) and (there is a Customer in the Customer Line):
# 	    Pop Teller from the Teller Line.
# 	    Pop Customer from the Customer Line.
#       Adjust Teller’s time to when the Teller will next be available.
#       Add Teller back into Teller Line.
#
# 	If at end of day, Customers are in Customer Line:
# 		Update the necessary metrics
#
# 	If at end of day, Tellers are in Teller Line:
# 		Update the necessary metrics

# Assumptions
#   1. After closing, tellers will finish helping customers that are in the process of being helped.
#   2. After closing, tellers will not help customers still standing in line.
#   3. Priority customers are ONLY helped by priority tellers. 
#   4. Standard customers are ONLY helped by standard tellers.

from queue import PriorityQueue
import heapq
import copy
import random


class Customer:
    def __init__(self, time, work, type):
        self.time = time        # Arrival time.
        self.work = work        # Units of work required to help customer.
        self.type = type        # 'p' for priority, 's' for standard.

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __gt__(self, other):
        return self.time > other.time


class Teller:
    def __init__(self, time, workRate, type):
        self.time = time            # Time that teller becomes available.
        self.workRate = workRate    # Units/hour
        self.type = type            # 'p' for priority, 's' for standard.

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __lt__(self, other):
        return self.time < other.time


# Queues
stanLine = PriorityQueue()          # Stores all standard customers
priLine = PriorityQueue()           # Stores all priority customers
priTellerLine = PriorityQueue()     # Stores all tellers
stanTellerLine = PriorityQueue()    # Stores all tellers

# Global variables.
priCustomerCount = 0            # Number of priority customers in all sims
priCustomerServed = 0           # Number of prioirty customers served in all sims
priCustomerWait = 0             # Time all priority customers spent waiting in line in all sims

stanCustomerCount = 0           # Number of standard customers in all sims
stanCustomerServed = 0          # Number of standard customers served in all sims
stanCustomerWait = 0            # Time all standard customers spent wainting in line in all sims

stanTellerIdleTime = 0          # Time all standard tellers spent not helping customers in all sims
priTellerIdleTime = 0           # Time all priority tellers spent not helping customers in all sims

customerWorkAvg = 5             # Mean of customer work gaussian distribution
customerWorkStdDev = 2.5        # Std deviation of customer work gaussian distribution
customerWorkUpperLimit = 15     # Customers will not request more than 15 units of work
customerWorkLowerLimit = 2      # Customers will not request less than 2 units of work

workingHours = 8                # Tellers will not help customers after working hours.


def main():

    simulations = 100
    
    print("\nEach scenario is ran", simulations, "time(s). \nThe following metrics are the avearage of all simulations.\n")


    # 8, 9, 10, 11, 12 Standard Tellers, 0 Priority Tellers
    numCustomers = 160
    tellerWorkRate = 10

    numPriTellers = 0
    priLineLimit = 0

    stanTellers = [9, 10, 11]

    for numStanTellers in stanTellers:
        print(numStanTellers, "tellers:")
        bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
        printMetrics(simulations)


    # 9 Standard Tellers, 1 Priority Teller
    numPriTellers = 1
    numStanTellers = 9
    priLineLimit = 3.1

    print("9 Standard tellers, 1 priority teller:")
    bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
    printMetrics(simulations)


# Truncated gaussian function
def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu, sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu, sigma)
    return a

# Print the list of Customers
def printCustomers():
    for i in range(priLine.qsize()):
        print(i, priLine[i].work)
    for i in range(stanLine.qsize()):
        print(i, stanLine[i].work)

# Initialize Customers
def initCustomers(numCustomers, priLineLimit):

    global priCustomerCount
    global stanCustomerCount
    global customerWorkAvg
    global customerWorkStdDev
    global customerWorkUpperLimit
    global customerWorkLowerLimit

    # Clear priority line.
    while not priLine.empty():
        try:
            priLine.get(False)
        except:
            continue
        priLine.task_done()

    # Clear standard line.
    while not stanLine.empty():
        try:
            stanLine.get(False)
        except:
            continue
        stanLine.task_done()

    # Add customer to priority or standard line.
    for i in range(numCustomers):
        work = trunc_gauss(customerWorkAvg, customerWorkStdDev, customerWorkLowerLimit, customerWorkUpperLimit)
        time = random.uniform(0, workingHours)

        if work <= priLineLimit:
            priLine.put(Customer(time, work, 'p'))
            priCustomerCount += 1
        else:
            stanLine.put(Customer(time, work, 's'))
            stanCustomerCount += 1
        #print(stanLine.queue[i].work)

# Initialize Tellers
def initTellers(priTellers, stanTellers, workRate):

    # Clear priority teller line.
    while not priTellerLine.empty():
        try:
            priTellerLine.get(False)
        except:
            continue
        priTellerLine.task_done()

    # Clear standard teller line.
    while not stanTellerLine.empty():
        try:
            stanTellerLine.get(False)
        except:
            continue
        stanTellerLine.task_done()

    for i in range(priTellers):
        priTellerLine.put(Teller(0, workRate, 'p'))
    for i in range(stanTellers):
        stanTellerLine.put(Teller(0, workRate, 's'))


def bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations):

    # Reset Simulation Metrics
    global priCustomerCount;    priCustomerCount = 0
    global stanCustomerCount;   stanCustomerCount = 0
    global priCustomerServed;   priCustomerServed = 0
    global stanCustomerServed;  stanCustomerServed = 0
    global priCustomerWait;     priCustomerWait = 0
    global stanCustomerWait;    stanCustomerWait = 0
    global priTellerIdleTime;   priTellerIdleTime = 0
    global stanTellerIdleTime;  stanTellerIdleTime = 0
    global workingHours


    for i in range(simulations):

        # Initialize Tellers and Customers
        initTellers(numPriTellers, numStanTellers, tellerWorkRate)
        initCustomers(numCustomers, priLineLimit)

        if numPriTellers > 0:
            priTeller = priTellerLine.queue[0]
        stanTeller = stanTellerLine.queue[0]

        # Help Customers in Priority Line
        while not priLine.empty() and priTeller.time <= workingHours:
            priCustomer = priLine.queue[0]
            priTeller = serveCustomer(priTeller, priCustomer, priTellerLine)

        # Help Customers in Standard Line
        while not stanLine.empty() and stanTeller.time <= workingHours:
            stanCustomer = stanLine.queue[0]
            stanTeller = serveCustomer(stanTeller, stanCustomer, stanTellerLine)

        # Calculate Metrics for Unserved Priority Customers
        while not priLine.empty():
            priCustomer = priLine.get()
            priCustomerWait += (workingHours - max(priCustomer.time, workingHours))

        # Calculate Metrics for Unserved Standard Customers.
        while not stanLine.empty():
            stanCustomer = stanLine.get()
            stanCustomerWait += (workingHours - max(stanCustomer.time, workingHours))

        # Calculate Metrics for Priority Tellers still waiting in line.
        while not priTellerLine.empty():
            priTeller = priTellerLine.get()

            if priTeller.time < workingHours:
                priTellerIdleTime += workingHours - priTeller.time

        # Calculate Metrics for Standard Tellers still waiting in line.
        while not stanTellerLine.empty():
            stanTeller = stanTellerLine.get()

            if stanTeller.time< workingHours:
                stanTellerIdleTime += workingHours - stanTeller.time


# Serve next customer. Return next teller.
def serveCustomer(teller, customer, line):
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait
    global stanTellerIdleTime
    global priTellerIdleTime

    # Teller is waiting for a customer.
    if (teller.time < customer.time):
        if teller.time < customer.time and teller.type == 'p':
            priTellerIdleTime += customer.time - teller.time
        if teller.time < customer.time and teller.type == 's':
            stanTellerIdleTime += customer.time - teller.time
        teller.time = customer.time

    # Past closing.
    if (teller.time > workingHours):
        return teller

    # Priority customer
    if (customer.type == 'p'):
        priLine.get()
        priCustomerServed += 1
        priCustomerWait += (teller.time-customer.time)
    else:  # Standard customer
        stanLine.get()
        stanCustomerServed += 1
        stanCustomerWait += (teller.time - customer.time)

    # Remove and replace teller at back of teller line.
    line.get()
    teller.time += (customer.work / teller.workRate)
    line.put(teller)

    return copy.copy(line.queue[0])


def printMetrics(simulations):
    print("\tStandard Customers Count:    ", stanCustomerCount/simulations)
    print("\tStandard Customers Unserved: ", (stanCustomerCount - stanCustomerServed)/simulations)
    print("\tStandard Customers Wait:     ", round(stanCustomerWait/stanCustomerCount, 4), "\n")

    if priCustomerCount > 0:
        print("\tPriority Customers Count:    ", priCustomerCount/simulations)
        print("\tPriority Customers Unserved: ", (priCustomerCount - priCustomerServed)/simulations)
        print("\tPriority Customers Wait:     ", round(priCustomerWait/priCustomerCount,4), "\n")

        print("\tTotal UNSERVED Customers:  ", (priCustomerCount + stanCustomerCount-priCustomerServed - stanCustomerServed)/simulations)
        print("\tTotal Customer Wait:       ", round((priCustomerWait + stanCustomerWait)/(priCustomerCount + stanCustomerCount), 4), '\n')

    print("\tStandard Teller Idle Time: ", round(stanTellerIdleTime/simulations, 4))

    if priCustomerCount > 0:
        print("\tPriority Teller Idle Time: ", round(priTellerIdleTime/simulations, 4))
        print("\tTotal Teller Idle Time:    ", round((priTellerIdleTime+stanTellerIdleTime)/simulations, 4))

    print()

main()

# reference
# https://stackoverflow.com/questions/16471763/generating-numbers-with-gaussian-function-in-a-range-using-python
# https://stackoverflow.com/questions/38560760/python-clear-items-from-priorityqueue
