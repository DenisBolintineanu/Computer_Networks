import heapq


class EventQueue:
    time = 0
    queue = []
    heapq.heapify(queue)

    @staticmethod
    def push(event):
        heapq.heappush(EventQueue.queue, event)

    @staticmethod
    def start():
        pass


# please implement here


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
