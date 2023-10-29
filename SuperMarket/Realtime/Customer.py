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

    def __init__(self, purchase_list, name, start_time):
        self.list = list(purchase_list)
        self.name = name
        self.start_time = start_time
        Customer.count += 1
        self.number = Customer.count
        self.actual_task = None
        self.complete = True
        self.total_time = 0
        self.thread = threading.Thread(target=Customer.go_to_station)
        self.condition = threading.Condition

    def run(self):
        self.thread.run()

    def go_to_station(self):
        self.actual_task = self.list.pop(0)
        time.sleep(self.actual_task[0])
        self.arrive_station(0)


    def arrive_station(self, t):
        self.actual_task[1].queue(self.actual_task[2])
        if self.actual_task[1].customers >= self.actual_task[3]:
            self.dropped[self.actual_task[1].name] += 1
            self.leave_station(t)
            self.complete = False
        else:
            EventQueue.push(Event(t + self.actual_task[1].waiting_time, self.leave_station, t + self.actual_task[1].waiting_time, 1))
            self.total_time += self.actual_task[1].waiting_time
            self.served[self.actual_task[1].name] += 1

    def leave_station(self, t):
        self.actual_task[1].dequeue(self.actual_task[2])
        if self.list:
            self.actual_task = self.list.pop(0)
            EventQueue.push(Event(t + self.actual_task[0], self.arrive_station, t + self.actual_task[0], 2))
        else:
            Customer.duration += self.total_time
            if self.complete:
                Customer.complete += 1
                Customer.duration_cond_complete += self.total_time
