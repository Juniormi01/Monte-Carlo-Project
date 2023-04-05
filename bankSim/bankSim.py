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
priTellerLine = PriorityQueue()     # Stores all tellers
stanTellerLine = PriorityQueue()    # Stores all tellers

# Global variables.
priCustomerCount = 0        
priCustomerServed = 0
priCustomerWait = 0

stanCustomerServed = 0
stanCustomerWait = 0
stanCustomerCount = 0       

closingTime = 8         # Tellers will not help customers after closing time.

# Initialize Customers
# NOTE customers need truncation [5,15]!!!!!!!!!!!!!!!!!!!!!!!!!!
def initCustomers(numCustomers, priLineLimit):
    global priCustomerCount 
    global stanCustomerCount 

    for i in range(numCustomers):
        work = random.gauss(5, 0.5)
        time = random.uniform(0,8)
        if work <= priLineLimit:
            priLine.put(Customer(time, work, 'p'))
            priCustomerCount +=1
        else:
            stanLine.put(Customer(time, work, 's'))
            stanCustomerCount +=1

def initTellers(priTellers, stanTellers, workRate):
    for i in range(priTellers):
        priTellerLine.put(Teller(0, workRate, 'p'))
    for i in range(stanTellers):
        stanTellerLine.put(Teller(0, workRate, 's'))

def bankSimulation():
    global priCustomerServed
    global stanCustomerServed
    global priCustomerWait
    global stanCustomerWait
    global closingTime

    priTeller = priTellerLine.queue[0]
    stanTeller = stanTellerLine.queue[0]

    # Priority Line
    while not priLine.empty() and priTeller.time <= closingTime:
        priCustomer = priLine.queue[0]
        priTeller = serveCustomer(priTeller, priCustomer, priTellerLine)

    # Standard Line
    while not stanLine.empty() and stanTeller.time <= closingTime:
        stanCustomer = stanLine.queue[0]
        stanTeller = serveCustomer(stanTeller, stanCustomer, stanTellerLine)

    # Unserved priority customer wait time.
    while not priLine.empty():
        priCustomer = priLine.get()
        priCustomerWait += (closingTime - max(priCustomer.time, closingTime))

    # Unserved standard customer wait time.
    while not stanLine.empty():
        stanCustomer = stanLine.get()
        stanCustomerWait += (closingTime - max(stanCustomer.time, closingTime))
 
# Serve next customer. Return next teller.
def serveCustomer(teller, customer, line):
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait 
    
    # Teller is waiting for a customer.
    if (teller.time < customer.time):
        teller.time = customer.time

    # Past closing.
    if (teller.time > closingTime):
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


def printMetrics():
    print("Standard Customers Count:  ", stanCustomerCount)
    print("Standard Customers Served: ", stanCustomerServed)
    print("Standard Customers Wait:   ", stanCustomerWait, "\n")

    print("Priority Customers Count:  ", priCustomerCount)
    print("Priority Customers Served: ", priCustomerServed)
    print("Priority Customers Wait:   ", priCustomerWait)

def main():
    numPriTellers = 2
    numStanTellers = 8
    tellerWorkRate = 10

    numCustomers = 160
    priLineLimit = 4.7      # Customer work limit to be placed in the priority line.

    for i in range(1):
        initTellers(numPriTellers, numStanTellers, tellerWorkRate)
        initCustomers(numCustomers, priLineLimit)
        bankSimulation()
    
    printMetrics()

main()
