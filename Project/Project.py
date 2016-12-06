from random import random, choice
from math import log

TOLERANCE = 1e-10
DEBUG = False
LAMBDA = 0.9722
MIU = 1.0 / 2

TOTAL_TIME = 6 * 60


RANDOM_CHOICE_SERVER = True
STR_CHOICE = ''

HEADER_SIM = False
HEADER_STATS = False

def exponential(lambda_):
    return - log (random()) / lambda_

class Customer():
    def __init__(self):
        self.arrivalDepartureTime = list()

class Server():
    def __cmp__(self, other):
        ''' How the servers are compared '''
        return len(self.queue) - len(other.queue)

    def __init__(self, index):
        self.miu = MIU
        self.queue = list()
        self.arrivals = 0
        self.departures = 0
        self.isBusy = False
        self.inDeparture = False
        self.index = index

        #Busy Time server
        self.busyTime = 0.0

class System():
    def __init__(self, numberServers):
        self.t = 0.0
        self.N = 0
        self.servers = list()
        self.departureEvent = list()
        self.departures = 0
        self.arrivals = 0

        for s in xrange(numberServers):
            self.servers.append(Server(s))

    def mechanismToSelectServer(self):
        if RANDOM_CHOICE_SERVER:
            #random choice of server
            return self.randomServerChoice()
        else:
            #shortest queue length
            return self.shortestQueue()

    def randomServerChoice(self):
        return choice(self.servers)

    def shortestQueue(self):
        return min(self.servers)

    def selectServer(self, customer):
        server = self.mechanismToSelectServer()
        server.queue.append(customer)
        if DEBUG:
            print "in Server",server.index
        if not server.isBusy:
            server.isBusy = True
            server.arrivals += 1

    def update(self):
        if self.t == 0:
            self.t = exponential(LAMBDA)
            self.newArrival()
        else:
            arrivalTime = self.t + exponential(LAMBDA)

            i = 0
            for s in self.servers:
                if s.isBusy and not s.inDeparture:
                    nextDepartureTime = self.t + exponential(s.miu)
                    self.departureEvent.append([nextDepartureTime, i])

                    s.queue[0].arrivalDepartureTime.append(self.t)
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
            print "New Arrival at", self.t,
        self.arrivals += 1
        customer = Customer()
        customer.arrivalDepartureTime.append(self.t)
        self.selectServer(customer)

    def newDeparture(self, serverIndex):
        global HEADER_SIM
        if DEBUG:
            print "New Departure from server %d at %f" % (serverIndex, self.t)
        self.departures += 1
        server = self.servers[serverIndex]
        customer = server.queue.pop(0)
        customer.arrivalDepartureTime.append(self.t)
        saveFile = open('sim.csv', 'a')
        if not HEADER_SIM:
            print>>saveFile, 'serverChoice,numberOfServers,ServerIndex,ArrivalTime,startServerTime,DepartureTime'
            HEADER_SIM = True
        #serverChoice,numberOfServers,ServerIndex,ArrivalTime,startServerTime,DepartureTime
        print>>saveFile, "%s,%d,%d,%.20f,%.20f,%.20f" % (STR_CHOICE,len(self.servers),serverIndex, customer.arrivalDepartureTime[0],customer.arrivalDepartureTime[1],customer.arrivalDepartureTime[2])
        saveFile.close()
        server.departures += 1
        server.isBusy = False
        server.inDeparture = False

    def sim(self, totalTime):
        while self.t < totalTime:
            self.update()
        return (self.departures, self.arrivals)

def main():
    global RANDOM_CHOICE_SERVER, STR_CHOICE
    global HEADER_STATS

    rep = 50
    maxServers = 15


    for choice in [True, False]:
        RANDOM_CHOICE_SERVER = choice

        if RANDOM_CHOICE_SERVER:
            STR_CHOICE = 'Random'
        else:
            STR_CHOICE = 'Minimum'

        for n in xrange(1, maxServers + 1):
            s = (0.0, 0.0)
            for r in xrange(rep):
                S = System(n)
                stats = S.sim(TOTAL_TIME)
                s = tuple(map(lambda x, y: x + y, stats, s))

                servicePercentage = 1.0 * stats[0] / stats[1] * 100
                saveFile = open('stats.csv', 'a') # file to save the performance of the system
                if not HEADER_STATS:
                    print>>saveFile, 'serverChoice,numberServers,servicePercentage'
                    HEADER_STATS = True
                #serverChoice,numberServers,servicePercentage
                print>>saveFile,'%s,%d,%.20f' % (STR_CHOICE, n, servicePercentage)


            # MEan services time
            m = tuple(map(lambda x: x / rep, s))

            servicePercentage = m[0] / m[1] * 100
            print 'Service percentace with %d servers: %.3f' % (n, servicePercentage)

            '''
            saveFile = open('stats.csv', 'a') # file to save the performance of the system
            #serverChoice,numberServers,servicePercentage
            print>>saveFile,'%s,%d,%.20f' % (STR_CHOICE, n, servicePercentage)
            '''

if __name__ == "__main__":
    main()
