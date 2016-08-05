class SampleSpace(dict):
    def __init__ (self):
        self.events = list()

    def addEvent(self, e):
        self.events.append(e)

class Event(set):
    def __init__ (self, space = None):
        self.sampleSpace = space
        set.__init__(self)

    def empty(self):
        '''check if the set is empty'''
        return len(self) == 0

    def complement(self):
        if self.sampleSpace is None:
            return None
        else:
            return set(self.sampleSpace.keys()) - self

    def union(self, event):
        if self.sampleSpace == event.sampleSpace:
            return self | event
        return False

    def intersection(self, e):
        if self.sampleSpace == event.sampleSpace:
            return self & event
        return False

def main():
    S = SampleSpace()
    S[1] = 0.1
    S[2] = 0.2
    S[3] = 0.4
    S[4] = 0.3

    A = Event(S)
    print A.empty()
    A.add(1)
    A.add(2)
    print A.empty()
    S.addEvent(A)

    B = Event(S)
    print B.empty()
    B.add(3)
    B.add(4)
    print B.empty()
    S.addEvent(B)
    print S
    print A.complement()
    print B.complement()

if __name__ == "__main__":
    main()
