import heapq


class EventQueue:
    time = 0

    def __init__(self):
        self.queue = []
        heapq.heapify(self.queue)

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)
