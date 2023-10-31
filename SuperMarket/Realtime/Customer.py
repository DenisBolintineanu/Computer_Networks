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
    start_time_clock = time.time()

    def __init__(self, purchase_list, name, start_time):
        self.list = list(purchase_list)
        self.name = name
        self.start_time = start_time
        Customer.count += 1
        self.number = Customer.count
        self.actual_task = None
        self.complete = True
        self.total_time = 0
        self.condition = threading.Condition
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.go_to_station).start()

    #def run(self):
    #   self.thread.run()

    def go_to_station(self):
        self.actual_task = self.list.pop(0)
        print("time: " + str(round(time.time() - Customer.start_time_clock, 0))+ ": customer " + str(self.number) + " go to " + self.actual_task[1].name)
        time.sleep(self.actual_task[0])
        print("time: " + str(round(time.time() - Customer.start_time_clock, 0))+ ": customer " + str(self.number) + " arrived at " + self.actual_task[1].name)
        self.arrive_station(0)

    def arrive_station(self, t):
        self.queue(self.actual_task[1], self.actual_task[2])
        if self.actual_task[1].customers >= self.actual_task[3]:
            Customer.dropped_lock.acquire()
            Customer.dropped[self.actual_task[1].name] += 1
            Customer.dropped_lock.release()
            self.actual_task[1].dropped()
            self.leave_station(t)
            self.complete = False
        else:
            self.total_time += self.actual_task[1].waiting_time
            Customer.served_lock.acquire()
            Customer.served[self.actual_task[1].name] += 1
            Customer.served_lock.release()
            
            #self.actual_task[1].serve()

    def leave_station(self, t):
        #self.dequeue(self.actual_task[1], self.actual_task[2])
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


    def queue(self, station, amount):
            station.lock.acquire()
            station.customers += 1
            station.waiting_time += station.runtime * amount
            station.lock.release()
            station.ev_queue.push(Event(self ,time.time(), self.arrive_station, self.actual_task[2], 2))
            station.threading_event.set()

    #dequeu benötigen wir eigentlich nicht mehr, da wir einfach in der Station selber runterzählen
    def dequeue(self, station):
        station.lock.acquire()
        station.customers -= 1
        #station.waiting_time -= station.runtime * amount
        station.lock.release()

