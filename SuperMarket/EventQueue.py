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
        for i in EventQueue.queue:
            event = heapq.heappop(EventQueue.queue)
            if event.args == ():
                event.work()
            else:
                event.work(event.args)
