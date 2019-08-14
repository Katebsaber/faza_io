from __future__ import print_function
from websocket import WebSocketApp
from kafka import KafkaProducer
import time
import pytz
from utility import _current_time_stamp, _utc_timestamp
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def _on_message(self, evt):
    producer.send('test', key=b'tBTCUSD', value=evt.encode('utf-8'))
    print(evt)


ws = WebSocketApp('wss://api-pub.bitfinex.com/ws/2')

ws.on_open = lambda self: self.send('{"event": "subscribe", "channel": "book", "symbol": "tBTCUSD", "prec": "P0", "freq": "F0", "len": 25}')
ws.on_message = _on_message
ws.run_forever()


