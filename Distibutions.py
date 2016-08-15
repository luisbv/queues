from random import random, randint
import BasicProbability as bs
class Distribution():
    def __init__(self):
        print "Distribution"
    def random(self):
        return random
    def sample(self, size):
        return [self.random() for x in xrange(size)]

class Bernoulli(Distribution):
    def __init__(self, p):
        self.sucess = p

    def random(self):
        return 1*(random() <= self.sucess) # return 1 or 0

class Binomial(Bernoulli):
    def __init__(self, n, p):
        self.rep = n
        Bernoulli.__init__(self, p)
    def random(self):
        return sum([Bernoulli.random(self) for b in xrange(self.rep)])

class PseudoPoisson(Binomial):
    def __init__(self, lambda_):
        n = 10000
        p = 1.0 * lambda_ / n
        print lambda_, n, p
        Binomial.__init__(self, n, p)

    def random(self):
        return Binomial.random(self)

class Multinomial(Binomial):
    def __init__(self, n, events):
        self.multi = dict()
        for event in events:
            print event
            for k in event:
                p = event[k]
                Binomial.__init__(self, n, p)
                self.multi[k] = Binomial.random(self)

    def random(self):
        return self.multi

class Geometric(Bernoulli):
    def __init__(self, p):
        Bernoulli.__init__(self,p)
    def random(self):
        counter = 0

        while Bernoulli.random(self) == 0:
            counter += 1

        return counter

class NegBin(Geometric):
    def __init__(self, n, p):
        self.n = n
        Geometric.__init__(self, p)
    def random(self):
        return sum([Geometric.random(self) for x in xrange(self.n)])

class UniformInteger(Distribution):
    def __init__(self, A = 0, B = 10):
        self.initial = A
        self.final = B

    def random(self):
        return randint(self.initial, self.final)

class PseudoUniform(UniformInteger):
    def __init__(self, N=100):
        self.N = N
        self.M = sum([UniformInteger().random() for x in xrange(self.N)])
        #UniformInteger.__init__(self)

    def sample(self, N=None):
        if N is None:
            N = self.N
        k = int(self.M / N) # particles
        r = self.M % N      # residual particles
        b = int(r)               # cells with k + 1 particles
        a = int(N - r)      # cells with k particles
        values = list() # values
        if r < N / 2.0:
            #add
            add = list()
            for n in xrange(N):
                values.append(k)

            for j in xrange(b):
                while True:
                    indexRandCell = randint(0, N - 1)
                    if indexRandCell not in add:
                        values[indexRandCell] += 1
                        add.append(indexRandCell)
                        break
        else:
            #remove
            remove = list()
            for n in xrange(N):
                values.append((k+1))

            for j in xrange(a):
                while True:
                    indexRandCell = randint(0, N - 1)
                    if indexRandCell not in remove:
                        values[indexRandCell] -= 1
                        remove.append(indexRandCell)
                        break
        return values

def main():
    d0 = UniformInteger()
    print "UniformInteger",d0.sample(20)
    d1 = PseudoUniform(20)
    print "PseudoUniform",d1.sample()
    d2 = Geometric(0.2)
    print "Geometric", d2.random()
    d3 = NegBin(4, 0.2)
    print "NegBin", d3.random()
    d4 = PseudoPoisson(10)
    print "PseudoPoisson", d4.random()
    d5 = Binomial(10,0.1)
    print "Binomial", d5.random()
    #Multinomial
    S = bs.SampleSpace()
    S[1] = 0.1
    S[2] = 0.2
    S[3] = 0.4
    S[4] = 0.3
    A = bs.Event(S)
    A.add(1) # add result 1 to event A
    A.add(2) # add result 2 to event A
    S.addEvent(A) # add event to the sample space

    # Same process for event A
    B = bs.Event(S)
    B.add(3)
    B.add(4)
    S.addEvent(B) # add event to the sample space

    d6 = Multinomial(10, [A,B])
    print "Multinomial", d6.random()
if __name__ == "__main__":
    main()
