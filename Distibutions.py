from random import random, randint
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
    def __init__(self):
        print "not available"
    #

class Multinomial():
    def __init__(self, events):
        print "not available"

    def random(self):
        #return dictionary
        return


class Geometric():
    #regresar contador hasta que hay un exito en Bernoulli
    #hacer prueba unitaria para comprobar su prob sin memoria
    def __init__(self):
        print "not available"

class NegBin():
    #geometrica
    def __init__(self):
        print "not available"

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
        UniformInteger.__init__(self)

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
    print d0.random()
    d1 = PseudoUniform(20)
    print d1.sample()

if __name__ == "__main__":
    main()
