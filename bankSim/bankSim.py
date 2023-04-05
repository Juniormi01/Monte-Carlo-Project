# bankSimVersion3.py
# Bank-Queue-Simulation
# CSCI 154

# The following program simulates a bank queue.
# Assumptions
#   1. After closing, tellers will finish helping customers that are in the process of being helped.
#   2. After closing, tellers will not help customers still standing in line.
#   3. If a customer is in line after closing, the customer's wait time will be added to the total wait time.

from queue import PriorityQueue
import heapq
import copy

class Customer:
    def __init__(self, time, work):
        self.time = time
        self.work = work

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
        self.time = time
        self.workRate = workRate
        self.type = type

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


# Global Variables

# Maximum amount of work a priority customer can have
priLineWorkLimit = 10           

# Total number of customers.
stanCustomerCount = 5           
priCustomerCount = 5  

# Total number of standard customers that were helped by tellers.
stanCustomerServed = 0
priCustomerServed = 0

# Total wait time of all customers.
stanCustomerWait = 0
priCustomerWait = 0    

# Tellers will not serve customers after closing time.
closingTime = 10                

stanLine = PriorityQueue()      # Stores all standard customers
priLine = PriorityQueue()       # Stores all priority customers
tellerLine = PriorityQueue()    # Stores all tellers


# Initialize Customers
# for i in range(10):
#     customerLine.put(Customer(i, 5))
priLine.put(Customer(1, 10))
priLine.put(Customer(1, 10))
priLine.put(Customer(1, 10))
priLine.put(Customer(2, 10))
priLine.put(Customer(2, 10))
priLine.put(Customer(2, 10))
priLine.put(Customer(2, 10))
priLine.put(Customer(2, 10))

stanLine.put(Customer(1, 15))
stanLine.put(Customer(1, 15))
stanLine.put(Customer(1, 15))
# stanLine.put(Customer(3, 15))
# stanLine.put(Customer(3, 15))

# Initialize Tellers
workRate = 10
tellerLine.put(Teller(0, workRate, 'p'))
tellerLine.put(Teller(0, workRate, 's'))
tellerLine.put(Teller(0, workRate, 's'))


def bankSimulation():

    global closingTime
    global priCustomerServed
    global stanCustomerServed
    global priCustomerWait
    global stanCustomerWait

    teller = copy.copy(tellerLine.queue[0])

    # Condition 1: Both priority line and standard line has customers.
    while not priLine.empty() and not stanLine.empty() and teller.time <= closingTime:

        stanCustomer = stanLine.queue[0]
        priCustomer = priLine.queue[0]
        
        if stanCustomer.time < priCustomer.time:
            teller = advanceTellerTime(teller, stanCustomer)
        else:
            teller = advanceTellerTime(teller, priCustomer)

        # Serve priority customer.
        if teller.type == 'p':
            teller = serveCustomer(teller, priCustomer)
        # Serve standard customer if they have been waiting in line.
        elif teller.time >= stanCustomer.time:
            teller = serveCustomer(teller, stanCustomer)
        # First customer to arrive is served.
        else:   
            if stanCustomer.time < priCustomer.time:
                teller = serveCustomer(teller, stanCustomer)
            else:
                teller = serveCustomer(teller, priCustomer)

    # Condition 2: Only priority line has customers.
    while not priLine.empty() and stanLine.empty() and teller.time <= closingTime:

        priCustomer = priLine.queue[0]
        teller = advanceTellerTime(teller, priCustomer)
        teller = serveCustomer(teller, priCustomer)

    # Condition 3: Only standard line has customers.
    while priLine.empty() and not stanLine.empty() and teller.time <= closingTime:

        # Remove priority tellers from front of queue.
        while (teller.type == 'p'):
            tellerLine.get()
            teller = copy.copy(tellerLine.queue[0])

        stanCustomer = stanLine.queue[0]
        teller = advanceTellerTime(teller, stanCustomer)
        teller = serveCustomer(teller, stanCustomer)

    # Unserved priority customer wait time.
    while not priLine.empty():
        priCustomer = priLine.get()
        priCustomerWait += (closingTime - priCustomer.time)

    # Unserved standard customer wait time.
    while not stanLine.empty():
        stanCustomer = stanLine.get()
        stanCustomerWait += (closingTime - stanCustomer.time)


# If the teller is waiting for a customer to arrive, advance teller's time to the customer's time.
# Returns the next available teller.
def advanceTellerTime(teller, customer):
    while ((teller.time <= closingTime) and (teller.time < customer.time)):
        tellerLine.get()
        teller.time = customer.time
        tellerLine.put(teller)
        
        teller = copy.copy(tellerLine.queue[0])

    return copy.copy(tellerLine.queue[0])

# Remove customer form the queue and calculate the wait time.
# Return the next available teller.
def serveCustomer(teller, customer):
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait

    # Past closing.
    if (teller.time > closingTime):
        return copy.copy(tellerLine.queue[0])

    # Priority customer
    if (customer.work <= priLineWorkLimit):
        priLine.get()
        priCustomerServed += 1
        priCustomerWait += (teller.time-customer.time)
    else:  # Standard customer
        stanLine.get()
        stanCustomerServed += 1
        stanCustomerWait += (teller.time - customer.time)

    # Advance Teller
    tellerLine.get()
    teller.time += (customer.work / teller.workRate)
    tellerLine.put(teller)

    return copy.copy(tellerLine.queue[0])


def printMetrics():
    print("Standard Customers Count:  ", stanCustomerCount)
    print("Standard Customers Served: ", stanCustomerServed)
    print("Standard Customers Wait:   ", stanCustomerWait, "\n")

    print("Priority Customers Count:  ", priCustomerCount)
    print("Priority Customers Served: ", priCustomerServed)
    print("Priority Customers Wait:   ", priCustomerWait)


bankSimulation()
printMetrics()
