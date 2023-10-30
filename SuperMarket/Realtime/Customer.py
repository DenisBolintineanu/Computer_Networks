import time

from EventQueue import EventQueue
from Event import Event
import threading


class Customer:
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0
    served_lock = threading.Lock()
    dropped_lock = threading.Lock()
    duration_lock = threading.Lock()
    duration_complete_lock = threading.Lock()
    complete_lock = threading.Lock()

    def __init__(self, purchase_list, name, start_time):
        self.list = list(purchase_list)
        self.name = name
        self.start_time = start_time
        Customer.count += 1
        self.number = Customer.count
        self.actual_task = None
        self.complete = True
        self.total_time = 0
        self.thread = threading.Thread(target=self.go_to_station)
        self.condition = threading.Condition
        self.event = threading.Event()

    def run(self):
        self.thread.run()

    def go_to_station(self):
        self.actual_task = self.list.pop(0)
        print("customer " + str(self.number) + " go to " + self.actual_task[1].name)
        time.sleep(self.actual_task[0])
        print("customer " + str(self.number) + " arrived at " + self.actual_task[1].name)
        self.arrive_station(0)

    def arrive_station(self, t):
        self.actual_task[1].queue(self.actual_task[2])
        if self.actual_task[1].customers >= self.actual_task[3]:
            Customer.dropped_lock.acquire()
            Customer.dropped[self.actual_task[1].name] += 1
            Customer.dropped_lock.release()
            self.leave_station(t)
            self.complete = False
        else:
            self.total_time += self.actual_task[1].waiting_time
            Customer.served_lock.acquire()
            Customer.served[self.actual_task[1].name] += 1
            Customer.served_lock.release()
            self.actual_task[1].serve(self.event)

    def leave_station(self, t):
        self.actual_task[1].dequeue(self.actual_task[2])
        if self.list:
            self.go_to_station()
        else:
            Customer.duration_lock.acquire()
            Customer.duration += self.total_time
            Customer.duration_lock.release()
            if self.complete:
                Customer.complete_lock.acquire()
                Customer.complete += 1
                Customer.complete_lock.release()
                Customer.duration_complete_lock.acquire()
                Customer.duration_cond_complete += self.total_time
                Customer.duration_complete_lock.release()
