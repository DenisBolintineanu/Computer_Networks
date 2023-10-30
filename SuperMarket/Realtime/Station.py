import threading
from EventQueue import EventQueue


class Station:
    def __init__(self, runtime, name):
        self.thread = threading.Thread
        self.runtime = runtime
        self.name = name
        self.customers = 0
        self.waiting_time = 0
        self.threading_event = threading.Event()
        self.lock = threading.Lock()
        self.ev_queue = EventQueue()

    def queue(self, amount):
        self.lock.acquire()
        self.customers += 1
        self.waiting_time += self.runtime * amount
        self.lock.release()

    def dequeue(self, amount):
        self.lock.acquire()
        self.customers -= 1
        self.waiting_time -= self.runtime * amount
        self.lock.release()

    def serve(self, event):
        event.clear()

