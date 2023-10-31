class Event:
    counter = 0

    def __init__(self, customer, t, work, args=(), prio=255):
        self.t = t
        self.n = Event.counter
        self.work = work
        self.args = args
        self.prio = prio
        self.customer = customer
        Event.counter += 1

    def __lt__(self, other):
        if self.t < other.t:
            return True
        if self.t > other.t:
            return False
        if self.prio < other.prio:
            return True
        if self.prio > other.prio:
            return False
        if self.n < other.n:
            return True
        return False
