import threading
import time

from numpy import True_
from EventQueue import EventQueue


class Station:
    def __init__(self, runtime, name):
        self.runtime = runtime
        self.name = name
        self.customers = 0
        self.waiting_time = 0
        self.threading_event = threading.Event()
        self.lock = threading.Lock()
        self.lock_dropped = threading.Lock()
        self.ev_queue = EventQueue()
        self.thread = threading.Thread(target=self.serve).start()


    def serve(self):
        while True_:
            self.lock.acquire()
            if self.ev_queue.queue:
                task = self.ev_queue.pop()
                time.sleep(task.args*(self.runtime))
                self.dropped()
                print("leave station")
                #task.customer.dequeue(self)
                self.lock.release()
                task.customer.leave_station(0)
                
            else:
                self.lock.release()
                self.threading_event.wait()
            
    def dropped(self):
        with self.lock_dropped:
            self.customers -=1
