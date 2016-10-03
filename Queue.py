from random import choice
from Distributions import Exponential

DEBUG = False
LAMBDA = 10
MIU = 5

TOTAL_TIME = 50

class Customer():
    def __init__(self):
        self.arrivalDepartureTime = list()

class Server():
    def __init__(self, index):
        self.miu = MIU
        self.queue = list()
        self.arrivals = 0
        self.departures = 0
        self.isBusy = False
        self.inDeparture = False
        self.index = index

class Sistem():
    def __init__(self, numberServers):
        self.t = 0.0
        self.N = 0
        self.servers = list()
        self.departureEvent = list()
        self.departures = 0
        self.arrivals = 0

        for s in xrange(numberServers):
            self.servers.append(Server(s))

    def selectServer(self, customer):
        server = choice(self.servers)
        server.queue.append(customer)
        if DEBUG:
            print "in Server",server.index
        if not server.isBusy:
            server.isBusy = True
            server.arrivals += 1

    def update(self):
        if self.t == 0:
            self.t = Exponential(LAMBDA).random()
            self.newArrival()
        else:
            arrivalTime = self.t + Exponential(LAMBDA).random()

            i = 0
            for s in self.servers:
                if s.isBusy and not s.inDeparture:
                    self.departureEvent.append([self.t + Exponential(s.miu).random(), i])
                    s.inDeparture = True
                i += 1
            self.departureEvent = sorted(self.departureEvent)

            if len(self.departureEvent) > 0:
                if arrivalTime < self.departureEvent[0][0]:
                    self.t = arrivalTime
                    self.newArrival()
                else:
                    departureTime, serverIndex = self.departureEvent.pop(0)
                    self.t = departureTime
                    self.newDeparture(serverIndex)
            else:
                self.t = arrivalTime
                self.newArrival()

    def newArrival(self):
        if DEBUG:
            print "New Arrival at", t,
        self.arrivals += 1
        customer = Customer()
        customer.arrivalDepartureTime.append(self.t)
        self.selectServer(customer)

    def newDeparture(self, serverIndex):
        if DEBUG:
            print "New Departure from server %d at %f" % (serverIndex, t)
        self.departures += 1
        server = self.servers[serverIndex]
        customer = server.queue.pop(0)
        customer.arrivalDepartureTime.append(self.t)
        print "Server", serverIndex, "arrivalTime", customer.arrivalDepartureTime[0],"departureTime",customer.arrivalDepartureTime[1]
        server.departures += 1
        server.isBusy = False
        server.inDeparture = False

S = Sistem(5)

while S.t < TOTAL_TIME:
    S.update()
print S.departures, S.arrivals
