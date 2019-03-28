import gdax
import time
import pprint as pp
from datetime import datetime
import calendar
from pymongo import MongoClient


def iso8601_to_epoch(datestring):
    """
    iso8601_to_epoch - convert the iso8601 date into the unix epoch time
    >>> iso8601_to_epoch("2012-07-09T22:27:50.272517")
    1341872870
    """
    return calendar.timegm(datetime.strptime(
        datestring, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())


class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.mongo_client = MongoClient('mongodb://192.168.1.3:27017/')

        # specify the database and collection
        self.db = self.mongo_client.cryptocurrency_database
        self.BTC_collection = self.db.BTC_collection

        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and \
                'type' in msg and msg['type'] == 'match':
            parsed_t = iso8601_to_epoch(msg["time"])
            t_in_seconds = parsed_t

            self.BTC_collection.insert_one(
                {
                    "time": t_in_seconds,
                    "price": float(msg["price"]),
                    "size": float(msg["size"]),
                    "side": msg["side"]
                })
            print(
                "\tT ", t_in_seconds,
                "\tP {:.2f}".format(float(msg["price"])),
                "\tS {:.6f}".format(float(msg["size"])),
                "\t ", msg["side"])

    def on_close(self):
        print("-- Goodbye! --")


wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while True:
    #  print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()
