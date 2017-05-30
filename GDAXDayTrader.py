#import json
import time
import threading
import GDAX
import numpy as np

class MyWebsocketClient(GDAX.WebsocketClient):
    def __init__(self, url=None, products=None):
        super(MyWebsocketClient, self).__init__(url, products)
        self.completed_transactions = []
        self.lock = threading.Lock()

    def onOpen(self):
        self.completed_transactions = []
        print("Lets count the messages!")

    def onMessage(self, msg):
        if 'price' in msg and msg["type"] == "done" and msg["reason"] == "filled":
            self.lock.acquire()
            self.completed_transactions.append(msg)
            self.lock.release()

    def onClose(self):
        print("-- Goodbye! --")

def sell():
    print("sell")

def buy():
    print("buy")


ListOf = []

WSC = MyWebsocketClient(url="wss://ws-feed.gdax.com", products=["ETH-USD"])
WSC.start()

# Do some logic with the data
while True:
    time.sleep(10)
    WSC.lock.acquire()

    #print(json.dumps(WSC.completed_transactions, sort_keys=True, indent=4))
    for item in WSC.completed_transactions:
        print("Message type:", item["type"],
        ":", item["reason"], "\t@ %.3f" % float(item["price"] if 'price' in item else 0), "\t time:", item["time"])

    if len(WSC.completed_transactions) == 0:
        WSC.lock.release()
        continue

    price = [float(item["price"]) for item in WSC.completed_transactions]
    if len(price) == 0:
        print("error")

    meanVal = np.mean(price)
    ListOf.append(meanVal)
    longTermAverage = np.mean(ListOf)

    for a in ListOf:
        print(a, end=" ")

    if meanVal < longTermAverage:
        sell()
    else:
        buy()

    if len(ListOf) >= 10:
        del ListOf[0]

    WSC.completed_transactions = []
    WSC.lock.release()
WSC.close()
