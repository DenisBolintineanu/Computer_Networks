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

    def run(self):
        pass

