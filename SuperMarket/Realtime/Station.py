import threading

class Station:
    def __init__(self, runtime, name):
        self.runtime = runtime
        self.name = name
        self.customers = 0
        self.waiting_time = 0

    def queue(self, amount):
        self.customers += 1
        self.waiting_time += self.runtime * amount

    def dequeue(self, amount):
        self.customers -= 1
        self.waiting_time -= self.runtime * amount
