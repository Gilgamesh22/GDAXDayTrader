import time
import threading
import gdax
import numpy as np
import pandas as pd
import pprint as pp


class MyWebsocketClient(gdax.WebsocketClient):
    def __init__(self, url=None, products=None):
        super(MyWebsocketClient, self).__init__(url, products)
        self.message_count = 0
        self.completed_transactions = []
        self.lock = threading.Lock()

    def on_open(self):
        self.completed_transactions = []
        print("Lets count the messages!")

    def on_message(self, msg):
        if 'price' in msg and "type" in msg:
            self.lock.acquire()
            self.completed_transactions.append(msg)
            self.lock.release()

    def on_close(self):
        print("-- Goodbye! --")


class Wallet:
    """ETH Wallet"""
    def __init__(self):
        self.usd = 10000
        self.etc = 0
        self.purchase_price = 0

    def sell(self, val):
        """Sell ETH"""
        if self.etc > 0 and val > self.purchase_price:
            self.usd = self.etc * val
            self.etc = 0
            print("sell: USD:", self.usd, "ETC:", self.etc, "VAL", val)

    def buy(self, val):
        """buy ETH"""
        if self.usd > 0:
            self.etc = self.usd / val
            self.usd = 0
            self.purchase_price = val
            print("buy: USD:", self.usd, "ETC:", self.etc, "VAL", val)


ListOf = []
wallet = Wallet()
transactions = []

WSC = MyWebsocketClient(url="wss://ws-feed.gdax.com", products=["ETH-USD"])
WSC.start()

# Do some logic with the data
while True:
    time.sleep(30)
    WSC.lock.acquire()

    if not len(WSC.completed_transactions):
        WSC.lock.release()
        continue

    transactions = WSC.completed_transactions
    WSC.completed_transactions = []
    WSC.lock.release()

    price = [float(item["price"]) for item in transactions]
    if not price:
        print("error")

    # calculate rolling mean and determane whether to buy or sell
    meanVal = pd.rolling_mean(price, 12)
    ListOf.append(meanVal)
    longTermAverage = pd.rolling_mean(ListOf, 12)

    for a in ListOf:
        print(a, end=" ")
    print("")

    if len(ListOf) >= 12:
        if meanVal < longTermAverage:
            wallet.sell(meanVal)
        else:
            wallet.buy(meanVal)
        # delete oldest entry
        del ListOf[0]

WSC.close()
