from Customer import Customer
from EventQueue import EventQueue
from Station import Station
import pandas as pd
import threading
import time

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
        time.sleep(sT)
        while t < mT:
            customer = Customer(list(shopping_list), name + str(i), t)
            customer.run()
            i += 1
            t += dT
            time.sleep(dT)


    def start_purchase(time=30 * 60 + 1, interval_A=200, interval_B=60):
        baker = Station(10, 'Baker')
        butcher = Station(30, 'Butcher')
        cheese = Station(60, 'Cheese')
        cashier = Station(5, 'Cashier')
        Customer.served = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        Customer.dropped = {'Baker': 0, 'Butcher': 0, 'Cheese': 0, 'Cashier': 0}
        shopping_list1 = [(10, baker, 10, 10), (30, butcher, 5, 10), (45, cheese, 3, 5), (60, cashier, 30, 20)]
        shopping_list2 = [(30, butcher, 2, 5), (30, cashier, 3, 20), (20, baker, 3, 20)]
        threading.Thread(target=startCustomers, args=(shopping_list1, 'A', 0, interval_A, time)).start()
        threading.Thread(target=startCustomers, args=(shopping_list2, 'B', 1, interval_B, time)).start()

        """"
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
        """


    if __name__ == "__main__":
        x = start_purchase()
        """"
            print(x.loc['Average shopping duration'])
            for metric in METRICS:
                value = x.loc[metric].iloc[0]
                if 'duration' in metric:
                    my_print(f'{metric}: {value:.2f}s')
                else:
                    my_print(f'{metric}: {int(value)}')
        """