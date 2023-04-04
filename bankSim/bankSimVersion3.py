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
priLineWorkLimit = 10           # work limit for priority line

stanCustomerCount = 5           # Total number of standard customers.
# Total number of standard customers that were helped by tellers.
stanCustomerServed = 0
# Stores total wait time for all standard customers.
stanCustomerWait = 0

priCustomerCount = 5    # Total number of priority customers.
# Total number of priority customers that were helped by tellers.
priCustomerServed = 0
priCustomerWait = 0     # Stores total wait time for all priority customers.

closingTime = 3                 # Latest time customers will be helped.

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

stanLine.put(Customer(1, 15))
stanLine.put(Customer(1, 15))
stanLine.put(Customer(1, 15))
stanLine.put(Customer(3, 15))
stanLine.put(Customer(3, 15))

# Initialize Tellers
workRate = 10
tellerLine.put(Teller(0, workRate, 'p'))
tellerLine.put(Teller(0, workRate, 's'))
tellerLine.put(Teller(0, workRate, 's'))


def bankSimulation():
    global closingTime
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait

    # Condition 1: Priority line has customers. Standard line has customers.
    while not priLine.empty() and not stanLine.empty() and not tellerLine.empty():

        stanCustomer = stanLine.queue[0]
        priCustomer = priLine.queue[0]
        teller = copy.copy(tellerLine.queue[0])

        if stanCustomer.time < priCustomer.time:
            advanceTellerTime(teller, stanCustomer)
        else:
            advanceTellerTime(teller, priCustomer)

        if tellerLine.empty():
            break
        else:
            teller = copy.copy(tellerLine.queue[0])

        # Teller is open when customer(s) arrives.
        if (teller.time <= priCustomer.time and teller.time <= stanCustomer.time):
            if (priCustomer.time <= stanCustomer.time):
                serveCustomer(teller, priCustomer)
            else:
                serveCustomer(teller, stanCustomer)

        else:   # Both customers are waiting in line
            if teller.type == 's':
                serveCustomer(teller, stanCustomer)
            else:
                serveCustomer(teller, priCustomer)

    # Condition 2: Only priority line has customers.
    while not priLine.empty() and stanLine.empty() and not tellerLine.empty():

        priCustomer = priLine.queue[0]
        teller = copy.copy(tellerLine.queue[0])

        advanceTellerTime(teller, priCustomer)
        if tellerLine.empty():
            break
        else:
            teller = copy.copy(tellerLine.queue[0])
        # Note... MOVING THE ABOVE TELLER STATEMENT INTO advanceTellerTime changes the run time... figure out why
        serveCustomer(teller, priCustomer)

    # Condition 3: Only standard line has customers.
    while priLine.empty() and not stanLine.empty() and not tellerLine.empty():

        stanCustomer = stanLine.queue[0]
        teller = copy.copy(tellerLine.queue[0])
        while (teller.type == 'p')
            tellerLine.pop()

        advanceTellerTime(teller, stanCustomer)
        if tellerLine.empty():
            break

        else:
            teller = copy.copy(tellerLine.queue[0])

        serveCustomer(teller, stanCustomer)

    # Add wait time of unserved priority customers.
    while not priLine.empty():
        priCustomer = priLine.get()
        priCustomerWait += (closingTime - priCustomer.time)

    # Add wait time of unserved standard customers.
    while not stanLine.empty():
        stanCustomer = stanLine.get()
        stanCustomerWait += (closingTime - stanCustomer.time)


# If the teller is waiting for a customer to arrive, advance teller's time to the customer's time.
def advanceTellerTime(teller, customer):
    while ((not tellerLine.empty()) and (teller.time < customer.time)):
        tellerLine.get()

        teller.time = customer.time
        if teller.time < closingTime:
            tellerLine.put(teller)


def serveCustomer(teller, customer):
    global priCustomerServed
    global priCustomerWait
    global stanCustomerServed
    global stanCustomerWait

    # Priority Customer
    if (customer.work <= priLineWorkLimit):
        priLine.get()
        priCustomerServed += 1
        priCustomerWait += (teller.time-customer.time)

    else:  # Standard Customer
        stanLine.get()
        stanCustomerServed += 1
        stanCustomerWait += (teller.time - customer.time)

    # Teller
    tellerLine.get()
    teller.time += (customer.work / teller.workRate)
    if teller.time < closingTime:
        tellerLine.put(teller)


def printMetrics():
    print("Standard Customers Count:  ", stanCustomerCount)
    print("Standard Customers Served: ", stanCustomerServed)
    print("Standard Customers Wait:   ", stanCustomerWait, "\n")

    print("Priority Customers Count:  ", priCustomerCount)
    print("Priority Customers Served: ", priCustomerServed)
    print("Priority Customers Wait:   ", priCustomerWait)


bankSimulation()
printMetrics()


# standard line should not be able to use priority line
