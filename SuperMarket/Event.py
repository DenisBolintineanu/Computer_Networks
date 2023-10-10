class Event:
    counter = 0

    def __init__(self, t, work, args=(), prio=255):
        self.t = t
        self.n = Event.counter
        self.work = work
        self.args = args
        self.prio = prio
        Event.counter += 1

    def __lt__(self, other):
        if self.t < other.t:
            return True
        if self.prio > other.prio:
            return True
        if self.counter < other.counter:
            return True
        return False

# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description