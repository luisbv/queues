from random import random
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
        Bernoulli.__init(self, p)
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
