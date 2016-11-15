from random import choice
from Distributions import Exponential
TOLERANCE = 1e-10
DEBUG = False
LAMBDA = 10
MIU = 5

TOTAL_TIME = 100

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

class CustomerSystem():
    def __cmp__(self, other):
        ''' How the customers are compared '''
        return self.arrivalTime - other.arrivalTime

    def __init__(self, gamma,t=0):
        self.arrivalTime = t + Exponential(gamma).random()
        self.waitingTime = 0.0
        self.serviceTime = 0
        self.serviceRequieremt = 0

    def departureTime(self):
        return self.arrivalTime + self.waitingTime + self.serviceTime

    def sojournTime(self):
        return self.waitingTime + self.serviceTime

class QueueSystem():
    def __init__(self, gamma=0.5, mu=0.5, s=10, n=20):
        '''
        System M/M/S/S/N
        gamma = arrival rate
        mu = departure rate
        s = numbers of servers
        n = numbers of customers
        '''
        self.gamma = gamma
        self.mu = mu
        self.s = s
        self.n = n
        self.t = 0

        self.rho = 1.0 * self.gamma / self.mu
        # CUSTOMERS
        # Create N customers (with exponential distribution)
        #self.customers = sorted([Exponential(self.gamma).random() for c in xrange(n)])
        self.customers = [CustomerSystem(self.gamma) for c in xrange(n)]
        self.arrivals = sorted([c.arrivalTime for c in self.customers])
        self.trys = 0
        self.rejects = 0

        # SERVERS
        self.busyTime = 0
        self.startBusy = None
        self.departures = []

    def indexOfDepartures(self, departureTime):
        print departureTime, len(self.departures)
        for i in xrange(len(self.customers)):
            if abs(departureTime - self.customers[i].departureTime()) < TOLERANCE:
                return i

    def indexOfArrival(self, arrivalTime):
        for i in xrange(len(self.customers)):
            if abs(arrivalTime - (self.customers[i].arrivalTime + self.customers[i].waitingTime)) < TOLERANCE:
                return i

    def newArrival(self):
        self.t = self.arrivals.pop(0)
        index = self.indexOfArrival(self.t)
        print "Arrival", self.t, "Customer", index
        self.trys += 1

        # if the system is not bussy
        if len(self.departures) < self.s:
            # assign new departure time to the custumer
            self.customers[index].serviceTime = Exponential(self.mu).random()
            self.departures.append(self.t + self.customers[index].serviceTime)
            print "SetDeparture",self.departures[-1],"Customer",index
            #sort the departures
            self.departures.sort()
            # if the server is busy with the new arrival
            if len(self.departures) == self.s:
                #start the time that the system is busy
                self.startBusy = self.t
        else: # if the system is full
            # increment the rejects of customers
            self.rejects += 1
            # make new time for the customer to be server
            newTime = Exponential(self.gamma).random()
            self.arrivals.append(self.t + newTime)
            self.customers[index].waitingTime += newTime
            print "Set waitingTime",newTime,"New arrival",self.arrivals[-1],"Customer",index
            self.arrivals.sort()

    def newDeparture(self):

        self.t = self.departures.pop(0)

        index = self.indexOfDepartures(self.t)
        print "Departure", self.t, "Customer",index
        #self.customers.pop(index)
        # schedule new arrival
        self.customers.append(CustomerSystem(self.gamma, self.t))
        #print "new customer",self.customers[-1].arrivalTime
        self.arrivals.append(self.customers[-1].arrivalTime)
        self.arrivals.sort()

        # if the system is full
        if self.startBusy is not None:
            self.busyTime += self.t - self.startBusy
            self.startBusy = None

    def sim(self):
        while self.t < TOTAL_TIME:
            # if there are no departures
            # or (there are coustomers and
            # the next service is a customer arrival)
            if len(self.departures) == 0 or (len(self.arrivals) > 0 and self.arrivals[0] < self.departures[0]):
                self.newArrival()
            else:
                self.newDeparture()


    def simulation(self):
        while self.t < TOTAL_TIME:
            # if there are no departures
            # or (there are coustomers and
            # the next service is a customer arrival)
            if len(self.departures) == 0 or (len(self.arrivals) > 0 and self.arrivals[0] < self.departures[0]):
                # next time is arrival
                self.t = self.arrivals.pop(0)
                self.trys += 1

                # if the system is not bussy
                if len(self.departures) < self.s:
                    # assign new departure time to the custumer
                    self.departures.append(self.t + Exponential(self.mu).random())
                    #sort the departures
                    self.departures.sort()
                    # if the server is busy with the new arrival
                    if len(self.departures) == self.s:
                        #start the time that the system is busy
                        self.startBusy = self.t
                else: # if the system is full
                    # increment the rejects of customers
                    self.rejects += 1
                    # make new time for the customer to be server
                    self.arrivals.append(self.t + Exponential(self.gamma).random())
                    self.arrivals.sort()
            else: # if the next services is a departure
                self.t = self.departures.pop(0)
                # schedule new arrival
                self.arrivals.append(self.t + Exponential(self.gamma).random())
                self.arrivals.sort()

                # if the system is full
                if self.startBusy is not None:
                    self.busyTime += self.t - self.startBusy
                    self.startBusy = None

            print self.t

    def meanSojournTime(self):
        n = 0
        s = 0.0
        for c in self.customers:
            if c.sojournTime() <= TOTAL_TIME:
                n += 1
                s += c.sojournTime()

        return 1.0 * s / n
        #return sum([c.sojournTime() for c in self.customers]) / len(self.customers)

    def meanWaitingTime(self):
        n = 0
        s = 0.0
        for c in self.customers:
            if c.arrivalTime + c.waitingTime <= TOTAL_TIME:
                n += 1
                s += c.waitingTime

        return 1.0 * s / n
        #return sum([c.waitingTime for c in self.customers]) / len(self.customers)

    def meanServiceTime(self):
        n = 0
        s = 0.0
        for c in self.customers:
            if c.arrivalTime + c. waitingTime + c.serviceTime <= TOTAL_TIME:
                n += 1
                s += c.serviceTime

        return 1.0 * s / n
        #return sum([c.serviceTime for c in self.customers]) / len(self.customers)

    def expectedSojournTime(self):
        print "Entro"
        print self.mu
        return 1.0 / (self.mu - self.gamma)

    def expectedWaitingTime(self):
        return self.rho / (self.mu - self.gamma)

    def pkFormula(self):
        rho = 1.0 / self.mu
        E_S = self.meanServiceTime()
        E_N = rho / (1 - rho)
        E_T = 1.0 / (1 - rho) * E_S
        return E_N, E_T

def comparisonExpectedSojourn(replicas):
    mst = 0.0
    mwt = 0.0
    for r in xrange(replicas):
        QS = QueueSystem(0.6, 0.7, 1, 100000)
        QS.sim()
        mst += QS.meanSojournTime()
        mwt += QS.meanWaitingTime()
    #Distribution compared with expected
    print "sojournTime",mst / replicas,QS.expectedSojournTime()
    print "waitingTime",mwt / replicas,QS.expectedWaitingTime()

def comparisonPKFormula(replicas):
    # Pollaczek-Khinchin mean formula
    mn = 5
    mt = 0.0
    for r in xrange(replicas):
        QS = QueueSystem(0.01, 2.0, 1, mn)
        QS.sim()
        mt += QS.meanWaitingTime()
    #Distribution compared with expected
    E_N, E_T = QS.pkFormula()
    print "E_N", mn, E_N
    print "E_T", mwt / replicas, E_T


def main():
    '''
    S = System(5)

    while S.t < TOTAL_TIME:
        S.update()


    print S.departures, S.arrivals
    '''
    '''
    QS = QueueSystem(1.2, 2.0, 5, 10)
    QS.simulation()
    print 1.0 * QS.rejects / QS.trys, QS.busyTime / QS.t
    '''

    QS = QueueSystem(0.6, 0.7, 1, 10)
    QS.sim()



    #print sorted([c.sojournTime() for c in QS.customers]), QS.meanSojournTime()
    #print sorted([c.waitingTime for c in QS.customers]), QS.meanWaitingTime()
    #print sorted([Exponential(QS.mu - QS.gamma).random() for i in xrange(len(QS.customers))])
if __name__ == "__main__":
    #main()
    comparisonExpectedSojourn(10)
