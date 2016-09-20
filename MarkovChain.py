from random import random, choice
from Distributions import Exponential
threshold = 0.000001

class Markov(dict):
    def __init__(self):
        dict.__init__(self)
        self.state = None
        self.countVisits = dict()

    def addTransition(self, source, terminal, p):
        if source not in self:
            self[source] = dict()

        #check if the sum of probabilities of the init state exceed 1
        assert sum(self[source].values()) + p <= 1 + threshold
        if terminal not in self[source]:
            self[source][terminal] = p

        return


    def step(self, initial=None):
        if initial is None:
            if self.state is None:
                self.state = choice(self.keys())
                self.countVisits[self.state] = 1
                return self.state
        else:
            self.state = initial
            self.countVisits[self.state] = 1
            return self.state
        try:
            posibleMoves = self[self.state].keys()
        except:
            posibleMoves = list() #empty list
        r = random()
        choiced = self.state # default choice is the previous state
        pa = 0.0
        while len(posibleMoves) > 0 and pa < r:
            choiced = posibleMoves.pop(0)
            pa += self[self.state][choiced]


        self.state = choiced

        if self.state not in self.countVisits:
            self.countVisits[self.state] = 0
        self.countVisits[self.state] += 1
        return self.state


class MarkovProcess(dict):
    def __init__(self):
        dict.__init__(self)
        self.state = None
        self.timeVisits = dict()

    def addTransition(self, source, terminal, q):
        if source not in self:
            self[source] = dict()

        if terminal not in self[source]:
            self[source][terminal] = q

        return

    def step(self, initial=None):
        if initial is None:
            if self.state is None:
                self.state = choice(self.keys())
                return self.state
        else:
            self.state = initial
            return self.state
        minimum = 1e10
        #Select minimum waiting time
        for terminal in self[self.state]:
            q = self[self.state][terminal]
            waitingTime = Exponential(q).random()
            if waitingTime <= minimum:
                minimum = waitingTime
                choiced = terminal

        self.state = choiced
        if self.state not in self.timeVisits:
            self.timeVisits[self.state] = 0
        self.timeVisits[self.state] += minimum

        return self.state

class BirthDeath():
    def __init__(self, lambda_, mu, n=100):
        self.lambda_ = lambda_
        self.mu = mu
        self.n = n
        self.events = {"b": 0, "d": 0}
        self.probDeath = None
        self.probBirth = None
        self.timeVisits = dict()

    def start(self):
        self.t = 0.0
        self.i = self.n

    def birthRate(self):
        self.lambda_ *= 0
        return self.lambda_

    def deathRate(self):
        self.mu *= self.i
        return self.mu

    def step(self):
        self.totalRate = self.lambda_ + self.mu
        self.probBirth = 1.0 * self.lambda_ / self.totalRate
        self.probDeath = 1.0 * self.mu / self.totalRate

        if random() <= self.probDeath:
            self.events["d"] += 1
            duration = Exponential(self.mu).random()
            self.i -= 1
        else:
            self.events["b"] += 1
            duration = Exponential(self.lambda_).random()
            self.i += 1
        self.t += duration

    def simulation(self, maxTime=30):
        self.start()

        while self.i > 0 and self.t < maxTime:
            self.step()

        if self.i not in self.timeVisits:
            self.timeVisits[self.i] = 0
        self.timeVisits[self.i] += 1

class PoissonProcess():
    def __init__(self, lambda_):
        ''' interval from t1 to t2'''
        self.lambda_ = lambda_

    def arrivals(self, t1, t2):
        '''t2 = duration '''
        N = 0
        t = t1
        while t < t2:
            N += 1
            t += Exponential(self.lambda_).random()
        return N - 1

def main():
    print 'Markv Chain'
    M = Markov()
    ''' Transition Matrix
        a     b     c     d     e
    a  0.50  0.00  0.00  0.00  0.50
    b  0.00  0.50  0.00  0.50  0.00
    c  0.00  0.00  1.00  0.00  0.00
    d  0.00  0.25  0.25  0.25  0.25
    e  0.50  0.00  0.00  0.00  0.50
    '''
    M.addTransition("a", "e", 0.5)
    M.addTransition("b", "d", 0.5)
    M.addTransition("d", "b", 0.25)
    M.addTransition("d", "c", 0.25)
    M.addTransition("d", "e", 0.25)
    M.addTransition("e", "a", 0.5)

    STEPS = 20000
    M.step("d")
    for s in xrange(STEPS):
        M.step()

    print M.countVisits

    print
    print 'Markv process'
    MP = MarkovProcess()
    ''' Transition Matrix
        a     b     c     d
    a  0.00  1.20  3.20  1.80
    b  1.50  0.00  6.30  8.50
    c  8.90  6.00  0.00  2.60
    d  2.80  5.65  4.25  0.00
    '''
    MP.addTransition("a", "b", 1.20)
    MP.addTransition("a", "c", 3.20)
    MP.addTransition("a", "d", 1.80)
    MP.addTransition("b", "a", 1.50)
    MP.addTransition("b", "c", 6.30)
    MP.addTransition("b", "d", 8.50)
    MP.addTransition("c", "a", 8.90)
    MP.addTransition("c", "b", 6.00)
    MP.addTransition("c", "d", 2.60)
    MP.addTransition("d", "a", 2.80)
    MP.addTransition("d", "b", 5.65)
    MP.addTransition("d", "c", 4.25)

    STEPS = 20000
    MP.step("d")
    for s in xrange(STEPS):
        MP.step()

    print MP.timeVisits

    print
    print 'Birth Death Process'
    BD = BirthDeath(0, 0.1, 100)
    maxRep = 100
    for r in xrange(maxRep):
        BD.simulation(30)
    print sorted(BD.timeVisits)

    print
    print 'Poisson process'
    PP = PoissonProcess(10)
    print PP.arrivals(0.0,30)
if __name__ == "__main__":
    main()
