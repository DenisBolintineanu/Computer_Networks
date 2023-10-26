from Customer import Customer
from Event import Event
from EventQueue import EventQueue
from Station import Station

with open("supermarket.txt", "w") as f, open("supermarket_customer.txt", "w") as fc, open("supermarket_station.txt",
                                                                                          "w") as fs:
    # print on console and into supermarket log
    def my_print(msg):
        print(msg)
        f.write(msg + '\n')


    # print on console and into customer log
    # k: customer name
    # s: station name
    def my_print1(k, s, msg):
        t = EventQueue.time
        print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s)
        fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


    # print on console and into station log
    # s: station name
    # name: customer name
    def my_print2(s, msg, name):
        t = EventQueue.time
        print(str(round(t, 4)) + ':' + s + ' ' + msg)
        fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')


    def startCustomers(shopping_list, name, sT, dT, mT):
        i = 1
        t = sT
        while t < mT:
            customer = Customer(list(shopping_list), name + str(i), t)
            ev = Event(t, customer.run, prio=1)
            EventQueue.push(ev)
            i += 1
            t += dT


    def main():
        evQ = EventQueue()
        baker = Station(10, 'Baker')
        butcher = Station(30, 'Butcher')
        cheese = Station(60, 'Cheese')
        cashier = Station(5, 'Cashier')
        Customer.served = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        Customer.dropped = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        shopping_list1 = [(10, baker, 10, 10), (30, butcher, 5, 10), (45, cheese, 3, 5), (60, cashier, 30, 20)]
        shopping_list2 = [(30, butcher, 2, 5), (30, cashier, 3, 20), (20, baker, 3, 20)]
        startCustomers(shopping_list1, 'A', 0, 200, 30 * 60 + 1)
        startCustomers(shopping_list2, 'B', 1, 60, 30 * 60 + 1)
        evQ.start()
        my_print('End of simulation: %is' % EventQueue.time)
        my_print('Total customers: %i' % Customer.count)
        my_print('Total complete shopping: %i' % Customer.complete)
        x = Customer.duration / Customer.count
        my_print('Average shopping duration: %.2fs' % x)
        x = Customer.duration_cond_complete / Customer.complete
        my_print('Average shopping duration (complete): %.2fs' % x)
        S = ('Baker', 'Butcher', 'Cheese', 'Cashier')
        for s in S:
            x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
            my_print('Drop percentage at %s: %.2f' % (s, x))

        f.close()
        fc.close()
        fs.close()


    if __name__ == "__main__":
        main()
