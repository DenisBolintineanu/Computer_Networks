import heapq


class EventQueue:
    time = 0
    queue = []
    heapq.heapify(queue)

    def push(self, event):
        heapq.heappush(self.queue, event)

    def start(self):
        pass


# please implement here


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station

