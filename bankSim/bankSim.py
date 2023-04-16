# bankSim.py
# Bank-Queue-Simulation
# CSCI 154

# The following program simulates a bank queue.
# Assumptions
#   1. After closing, tellers will finish helping customers that are in the process of being helped.
#   2. After closing, tellers will not help customers still standing in line.
#   3. If a customer is in line after closing, the difference between the customer's wait time and the time the bank closed will be added to the total wait time.

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
tellerQueue = PriorityQueue()       # Stores all tellers

# Global variables.
priCustomerCount = 0
priCustomerServed = 0
priCustomerWait = 0

stanCustomerServed = 0
stanCustomerWait = 0
stanCustomerCount = 0

workHours = 8         # Tellers will not help customers after closing time.


def main():

        simulations = 10
        numCustomers = 160
        tellerWorkRate = 10
        
        
        
        print("\nEach scenario is ran", simulations, "time(s). \nThe following metrics are the avearage of all simulations.\n")

        # # 1 line, 9 tellers.
        # numPriTellers = 0
        # numStanTellers = 9
        # print("1 line, 9 tellers.")
        # bankSimulation(numPriTellers = 0, numStanTellers = 9, tellerWorkRate = 10, numCustomers = 160, priLineLimit = 0, simulations = 10)
        # printMetrics(simulations)

        # 1 line, 10 tellers.---------------------------------
        # numPriTellers = 0
        # numStanTellers = 10
        # priLineLimit = 0

        # print("1 line, 10 tellers.")
        # bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
        # printMetrics(simulations)

        # # 1 line, 11 tellers.-------------------------------------------
        # numPriTellers = 0
        # numStanTellers = 11
        # priLineLimit = 0

        # print("1 line, 11 tellers.")
        #bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
        # printMetrics(simulations)


        #2 lines, 1 priority teller, 9 standard tellers.
        numPriTellers = 1
        numStanTellers = 9
        priLineLimit = 5.1

        print("2 lines, 1 priority teller, 9 standard tellers.")
        bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
        printMetrics(simulations)

        # # 2 lines, 2 priority teller, 8 standard tellers.
        # numPriTellers = 2
        # numStanTellers = 8
        # priLineLimit = 5.1

        # print("2 lines, 2 priority tellers, 8 standard tellers")
        # bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations)
        # printMetrics(simulations)

       
# Initialize Customers
def initCustomers(numCustomers, priLineLimit):
    global priCustomerCount
    global stanCustomerCount

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
        work = trunc_gauss(5, 0.5, 5, 15)
        time = random.uniform(0, workHours)

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
    while not tellerQueue.empty():
        try:
            tellerQueue.get(False)
        except:
            continue
        tellerQueue.task_done()

    for i in range(priTellers):
        tellerQueue.put(Teller(0, workRate, 'p'))
    for i in range(stanTellers):
        tellerQueue.put(Teller(0, workRate, 's'))


def bankSimulation(numPriTellers, numStanTellers, tellerWorkRate, numCustomers, priLineLimit, simulations):

    # Reset Simulation
    global priCustomerCount;    priCustomerCount = 0
    global stanCustomerCount;   stanCustomerCount = 0
    global priCustomerServed;   priCustomerServed = 0
    global stanCustomerServed;  stanCustomerServed = 0
    global priCustomerWait;     priCustomerWait = 0
    global stanCustomerWait;    stanCustomerWait = 0
    global workHours

    for i in range(simulations):

        # Initialize Tellers and Customers
        initTellers(numPriTellers, numStanTellers, tellerWorkRate)
        initCustomers(numCustomers, priLineLimit)

        teller = tellerQueue.queue[0]

        # Priority Line and Standard Line both have customers.
        while not priLine.empty() and not stanLine.empty() and teller.time <= workHours:
            priCustomer = priLine.queue[0]
            stanCustomer = stanLine.queue[0]

            # Check if there are standard tellers available
            stanTellerAvailable = False
            for i in range(tellerQueue.qsize()):
                if tellerQueue.queue[i].type == 's':
                    stanTellerAvailable = True

            if stanTellerAvailable == False:
                break
                
            
            if priCustomer.time <= stanCustomer.time:
                teller = serveCustomer(teller, priCustomer)
            else:
                teller = serveCustomer(teller, stanCustomer)

        # Help Customers in Priority Line.
        while not priLine.empty() and teller.time <= workHours:
            priCustomer = priLine.queue[0]
            teller = serveCustomer(teller, priCustomer)

        # Help Customers in Standard Line.
        while not stanLine.empty() and teller.time <= workHours:
            stanCustomer = stanLine.queue[0]
            teller = serveCustomer(teller, stanCustomer)

        # Unserved priority customer wait time.
        while not priLine.empty():
            priCustomer = priLine.get()
            priCustomerWait += (workHours - max(priCustomer.time, workHours))

        # Unserved standard customer wait time.
        while not stanLine.empty():
            stanCustomer = stanLine.get()
            stanCustomerWait += (workHours - max(stanCustomer.time, workHours))


# Serve next customer. Return next teller.
def serveCustomer(teller, customer):
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait

    # Teller is waiting for a customer. Advance teller time.
    if (teller.time < customer.time):
            teller.time = customer.time

    # Past closing.
    if (teller.time > workHours):
        return teller

    # Condition 1: Priority teller and standard customer.
    if teller.type == 'p' and customer.type == 's':

        # Do not help customer. Advance teller time.
        tellerQueue.get()
        if not priLine.empty():
            teller.time = priLine.queue[0].time
            tellerQueue.put(teller)
        else:
            teller.time = workHours + 1
            tellerQueue.put(teller)

        return copy.copy(tellerQueue.queue[0])

    # Condition 2: Priorirty teller and prirority customer.
    if teller.type == 'p' and customer.type == 'p':

        # Help priority customer.
        priLine.get()
        priCustomerServed += 1
        priCustomerWait += (teller.time-customer.time)

        tellerQueue.get()
        teller.time += (customer.work / teller.workRate)
        tellerQueue.put(teller)
        return copy.copy(tellerQueue.queue[0])
    
    # Condition 3: Standard teller and priority customer.
    if teller.type == 's' and customer.type == 'p':

        # Help priority customer.
        priLine.get()
        priCustomerServed += 1
        priCustomerWait += (teller.time-customer.time)

        tellerQueue.get()
        teller.time += (customer.work / teller.workRate)
        tellerQueue.put(teller)
        return copy.copy(tellerQueue.queue[0])
    
    # Condition 4: Standarrd teller and standard customer.
    if teller.type == 's' and customer.type == 's':

        # Help standard customer.
        stanLine.get()
        stanCustomerServed += 1
        stanCustomerWait += (teller.time - customer.time)

        tellerQueue.get()
        teller.time += (customer.work / teller.workRate)
        tellerQueue.put(teller)
        return copy.copy(tellerQueue.queue[0])
    
    
# Print the averages of all metrics.
def printMetrics(simulations):
    print("\tStandard Customers Count:  ", stanCustomerCount/simulations)
    print("\tStandard Customers Served: ", stanCustomerServed/simulations)
    print("\tStandard Customers Wait:   ", stanCustomerWait/stanCustomerCount, "\n")

    if priCustomerCount > 0:
        print("\tPriority Customers Count:  ", priCustomerCount/simulations)
        print("\tPriority Customers Served: ", priCustomerServed/simulations)
        print("\tPriority Customers Wait:   ", priCustomerWait/priCustomerCount, "\n")

    print("\tTotal Customer Wait:        ", (priCustomerWait + stanCustomerWait)/(priCustomerCount + stanCustomerCount))
    print("\tTotal Customers NOT Served: ", (priCustomerCount + stanCustomerCount-priCustomerServed - stanCustomerServed)/simulations, "\n")

# Truncated gaussian function
def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu, sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu, sigma)
    return a

# Print list of Customers
def printCustomers():
    for i in range(priLine.qsize()):
        print(i, priLine[i].work)
    for i in range(stanLine.qsize()):
        print(i, stanLine[i].work)

main()

# reference
# https://stackoverflow.com/questions/16471763/generating-numbers-with-gaussian-function-in-a-range-using-python
# https://stackoverflow.com/questions/38560760/python-clear-items-from-priorityqueue
