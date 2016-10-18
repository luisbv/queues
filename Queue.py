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

        # CUSTOMERS
        # Create N customers (with exponential distribution)
        self.customers = sorted([Exponential(self.gamma).random() for c in xrange(n)])
        self.trys = 0
        self.rejects = 0

        # SERVERS
        self.busyTime = 0
        self.startBusy = None
        self.departures = []


    def simulation(self):
        while self.t < TOTAL_TIME:
            # if there are no departures
            # or (there are coustomers and
            # the next service is a customer arrival)
            if len(self.departures) == 0 or (len(self.customers) > 0 and self.customers[0] < self.departures[0]):
                # next time is arrival
                self.t = self.customers.pop(0)
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
                    self.customers.append(self.t + Exponential(self.gamma).random())
                    self.customers.sort()
            else: # if the next services is a departure
                self.t = self.departures.pop(0)
                # schedule new arrival
                self.customers.append(self.t + Exponential(self.gamma).random())
                self.customers.sort()

                # if the system is full
                if self.startBusy is not None:
                    self.busyTime += self.t - self.startBusy
                    self.startBusy = None

            print self.t






def main():
    '''
    S = System(5)

    while S.t < TOTAL_TIME:
        S.update()


    print S.departures, S.arrivals
    '''
    QS = QueueSystem(1.2, 2.0, 5, 10)
    QS.simulation()
    print 1.0 * QS.rejects / QS.trys, QS.busyTime / QS.t
if __name__ == "__main__":
    main()
