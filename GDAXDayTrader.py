import json
import GDAX
import time
import threading

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


WSC = MyWebsocketClient(url="wss://ws-feed.gdax.com", products=["ETH-USD"])
WSC.start()
# Do some logic with the data
while True:
    WSC.lock.acquire()
    #print(json.dumps(WSC.completed_transactions, sort_keys=True, indent=4))
    for msg in WSC.completed_transactions:
        print("Message type:", msg["type"], "\t@ %.3f" % float(msg["price"] if 'price' in msg else 0), "\t time:", msg["time"])

    WSC.completed_transactions = []
    WSC.lock.release()
    time.sleep(5)
WSC.close()



# Set a default product
PC = GDAX.PublicClient(api_url="https://api.gdax.com", product_id="ETH-USD")
#print(json.dumps(PC.getProducts(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductOrderBook(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductTicker(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductTrades(), sort_keys=True, indent=4))
#print(json.dumps(PC.getProductHistoricRates(granularity=1000 , start='2017-05-04', end='2017-05-05' ), sort_keys=True, indent=4))