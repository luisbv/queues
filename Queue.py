from random import choice
from Distributions import Exponential
from MarkovChain import PoissonProcess

LAMBDA = 5
MIU = 10

TIME_STEP = 0.1

TOTAL_STEPS = 100

TOTAL_WAITING_TIME = 0.0

class Client():
    def __init__(self, ):
        self.waitingTime = 0.0
        self.arrivalTime = 0.0

class Server():
    def __init__(self):
        self.miu = MIU
        self.queue = list()
        self.maxQueue = 1000
        self.serviceTime = 0.0
        self.exits = 0.0
        self.isBusy = False

    def setServiceTime(self):
        self.serviceTime = Exponential(self.miu).random()

    def incrementWaitingTimeCustomers(self, t):
        global TOTAL_WAITING_TIME
        for c in self.queue:
            c.waitingTime += t
            TOTAL_WAITING_TIME += t

class Sistem():
    def __init__(self, numberServers):
        self.t = 0.0
        self.clients = list()
        self.N = 0
        self.waitingTime = 0.0
        self.isArrival = False
        self.servers = list()

        for s in xrange(numberServers):
            self.servers.append(Server())

    def selectServer(self, customer):
        serverReceiver = choice(self.servers)
        if len(serverReceiver.queue) < serverReceiver.maxQueue:
            serverReceiver.queue.append(customer)
            if not serverReceiver.isBusy:
                serverReceiver.isBusy = True

    def updateTimeServers(self, t):
        for s in self.servers:
            if s.isBusy:
                s.serviceTime -= t
            if len(s.queue) > 0:
                s.incrementWaitingTimeCustomers(t)

    def step(self):
        if self.t == 0:
            self.N += 1
            self.t += Exponential(LAMBDA).random()
            c = Client()
            c.arrivalTime = self.t
            self.selectServer(c)
            self.isArrival = True
        else:
            newArrivalTime = Exponential(LAMBDA).random()

            newExitTime = 1000
            i = 0
            for s in self.servers:
                if s.isBusy:
                    if s.serviceTime == 0:
                        s.setServiceTime()
                        if s.serviceTime < newExitTime:
                            newExitTime = s.serviceTime
                            serverIndex = i
                    else:
                        if s.serviceTime < newExitTime:
                            newExitTime = s.serviceTime
                            serverIndex = i

                i += 1

            newTimes = [newArrivalTime, newExitTime]
            minTime = min(newTimes)
            if newTimes.index(minTime) == 0: # arrival
                self.N += 1
                self.updateTimeServers(newArrivalTime)
                self.t += newArrivalTime
                c = Client()
                c.arrivalTime = self.t
                self.selectServer(c)
                self.isArrival = True
            else:# departure
                self.t += newExitTime
                self.updateTimeServers(newExitTime)
                s = self.servers[serverIndex]
                s.queue.pop(0)
                s.exits += 1
                s.serviceTime = 0.0
                s.isBusy = False
                self.isArrival = False


S = Sistem(5)

for step in xrange(TOTAL_STEPS + 1):
    S.step()
    if step % 10 == 0:
        i = 0
        print "Step",step
        for server in S.servers:
            print "Server %d with %d clients in queque and %d clients servered" % (i, len(server.queue), server.exits)
            i += 1
        print

print "Expected Waiting Time", TOTAL_WAITING_TIME / S.N
