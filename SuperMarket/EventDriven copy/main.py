from Customer import Customer
from Event import Event
from EventQueue import EventQueue
from Station import Station
import pandas as pd

with open("supermarket.txt", "w") as f, open("supermarket_customer.txt", "w") as fc, open("supermarket_station.txt",
                                                                                          "w") as fs:
    METRICS = [
        'End of simulation',
        'Total customers',
        'Total complete shopping',
        'Average shopping duration',
        'Average shopping duration (complete)',
        'Drop percentage at Baker',
        'Drop percentage at Butcher',
        'Drop percentage at Cheese',
        'Drop percentage at Cashier'
    ]


    def my_print(msg):
        print(msg)
        f.write(msg + '\n')


    def startCustomers(shopping_list, name, sT, dT, mT):
        i = 1
        t = 0
        while i < 36:
            customer = Customer(list(shopping_list), name + str(i), t)
            ev = Event(t, customer.run, prio=1)
            EventQueue.push(ev)
            i += 1
            t += dT


    def start_purchase(time=30 * 60 + 1, interval_A=200, interval_B=60):
        evQ = EventQueue()
        baker = Station(0.1, 'Baker')
        butcher = Station(0.5, 'Butcher')
        cheese = Station(2.5, 'Cheese')
        cashier = Station(25, 'Cashier')
        Customer.served = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        Customer.dropped = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        shopping_list1 = [(0, baker, 1, 500), (0, butcher, 1, 4), (0, cheese, 1, 4), (0, cashier, 1, 2)]
        shopping_list2 = [(30, butcher, 2, 5), (30, cashier, 3, 20), (20, baker, 3, 20)]
        startCustomers(shopping_list1, 'A', 0, 0, time)
        #startCustomers(shopping_list2, 'B', 1, interval_B, time)
        evQ.start()

        return pd.DataFrame(
            {
                'Values': [
                    EventQueue.time,
                    Customer.count,
                    Customer.complete,
                    Customer.duration / Customer.count,
                    Customer.duration_cond_complete / Customer.complete,
                    Customer.dropped['Baker'] / (Customer.served['Baker'] + Customer.dropped['Baker']) * 100,
                    Customer.dropped['Butcher'] / (Customer.served['Butcher'] + Customer.dropped['Butcher']) * 100,
                    Customer.dropped['Cheese'] / (Customer.served['Cheese'] + Customer.dropped['Cheese']) * 100,
                    Customer.dropped['Cashier'] / (Customer.served['Cashier'] + Customer.dropped['Cashier']) * 100
                ]
            },
            index=METRICS
        )


    if __name__ == "__main__":
        x = start_purchase()
        print(30 * 60 + 1)
        print(x.loc['Average shopping duration'])
        for metric in METRICS:
            value = x.loc[metric].iloc[0]
            if 'duration' in metric:
                my_print(f'{metric}: {value:.2f}s')
            else:
                my_print(f'{metric}: {int(value)}')
