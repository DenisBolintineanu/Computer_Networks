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
        while EventQueue.queue:
            event = heapq.heappop(EventQueue.queue)
            EventQueue.time = event.t
            if event.args == ():
                event.work()
            else:
                event.work(event.args)
