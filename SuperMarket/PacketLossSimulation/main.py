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
        t = sT
        while i < 36:
            customer = Customer(list(shopping_list), name + str(i), t)
            ev = Event(t, customer.run, prio=1)
            EventQueue.push(ev)
            i += 1
            t += dT


    def start_purchase(time=0, interval_A=0, interval_B=60):
        evQ = EventQueue()
        baker = Station(10_000_0, 'Station1')
        butcher = Station(10_000_0, 'Station2')
        cheese = Station(1_000_0, 'Station3')
        cashier = Station(10_000_0, 'Station4')
        Customer.served = {'Station1': 0, 'Station2': 0, 'Station3': 0, 'Station4': 0}
        Customer.dropped = {'Station1': 0, 'Station2': 0, 'Station3': 0, 'Station4': 0}
        shopping_list1 = [(0, baker, 1, 500), (0, butcher, 1, 4), (0, cheese, 1, 4), (0, cashier, 1, 2)]
        startCustomers(shopping_list1, 'A', 0, 1, 0)
        evQ.start()

        return pd.DataFrame(
            {
                'Values': [
                    EventQueue.time,
                    Customer.count,
                    Customer.complete,
                    Customer.duration / Customer.count,
                    Customer.duration_cond_complete / Customer.complete,
                    Customer.dropped['Station1'] / (Customer.served['Station1'] + Customer.dropped['Station1']) * 100,
                    Customer.dropped['Station2'] / (Customer.served['Station2'] + Customer.dropped['Station2']) * 100,
                    Customer.dropped['Station3'] / (Customer.served['Station3'] + Customer.dropped['Station3']) * 100,
                    Customer.dropped['Station4'] / (Customer.served['Station4'] + Customer.dropped['Station4']) * 100
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
