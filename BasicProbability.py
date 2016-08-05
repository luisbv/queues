
class SampleSpace(dict):
    def __init__ (self):
        self.events = list()

    def addEvent(self, event):
        self.events.append(event)

class Event(dict):
    def __init__ (self, space = None, name = None):
        self.sampleSpace = space

    def add(self, result):
        if result not in self.keys():
            self[result] = self.sampleSpace[result]
        else:
            print "element %d already in event" % result

    def empty(self):
        '''check if the set is empty'''
        return len(self) == 0

    def complement(self):
        if self.sampleSpace is None:
            return None
        else:
            return set(self.sampleSpace.keys()) - set(self.keys())

    def union(self, event):
        if self.sampleSpace == event.sampleSpace:
            union = set(self.keys()) | set(event.keys())
            if len(union) == 0:
                print "Union is void"
                return False
            else:
                return union
        else:
            print "There is no union. Different sample space"
            return False

    def intersection(self, event):
        if self.sampleSpace == event.sampleSpace:
            intersection = set(self.keys()) & set(event.keys())
            if len(intersection) == 0:
                print "Intersection is void"
                return False
            else:
                return intersection
        else:
            print "There is no intersection. Different sample space"
            return False

def main():
    S = SampleSpace()
    S[1] = 0.1
    S[2] = 0.2
    S[3] = 0.4
    S[4] = 0.3

    A = Event(S)
    print "Event A is empty", A.empty() # check if event is empty
    A.add(1) # add result 1 to event A
    A.add(2) # add result 2 to event A
    A.add(1) # trying to add result 1 to event A
    print "Event A is empty", A.empty() # check if the event is empty one we add the results
    S.addEvent(A) # add event to the sample space

    # Same process for event A
    B = Event(S)
    print "Event B is empty", B.empty()
    B.add(3)
    B.add(4)
    print "Event B is empty", B.empty()
    S.addEvent(B)
    print "Sample Space", S # print sample space
    print "Intersection (A n B)", A.intersection(B)
    print "Intersection (B n A)", B.intersection(A)
    print "Union (A u B)", A.union(B), A.union(B)
    print "Union (B u A)", B.union(A)
    print "A complement", A.complement() # print complement of event A
    print "B complement",B.complement() # print complement of event B
    print "Event A", A # print event A
    print "Event B", B # print event B

if __name__ == "__main__":
    main()
