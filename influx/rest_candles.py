import time
from connector import create_record, check_point_existance, _utc_timestamp
from influxdb import InfluxDBClient
import requests
import urllib
import json
from sys import argv
from utility import _current_time_stamp

def _get_candles(end_timestamp, limit=1000, time_frame='1m', pair='tBTCUSD'):
    url = "https://api-pub.bitfinex.com/v2/candles/trade:{}:{}/hist?end={}&&limit={}".format(time_frame,pair,end_timestamp,limit)
    try:
        return requests.get(url).json()
    except Exception as e:
        print(e)

def _pars_candle(series_name: str, 
                    tags: dict,
                    record: list):
    try:
        return [
            {
                "measurement": series_name,
                "tags": tags,
                "time": _utc_timestamp(record[0]),
                "fields": {
                    'open':float(record[1]),
                    'close':float(record[2]),
                    'high':float(record[3]),
                    'low':float(record[4]),
                    'volume':float(record[5])
                }
            }
        ]   
    except Exception as e:
        print(e)

def main(client: InfluxDBClient, start_time_stamp: int):
    while start_time_stamp <= _current_time_stamp():
        if not check_point_existance(client, start_time_stamp,"candles"):
            candles = _get_candles(start_time_stamp)
            for each_candle in candles:
                json_body = _pars_candle('candle',{}, each_candle)
                print(json_body)
                create_record(client,json_body)
        start_time_stamp = list(client.query("select first(close) from candle",epoch='ms').get_points(measurement='candle'))[0]['time']
        time.sleep(5)
                

if __name__=='__main__':
    client = InfluxDBClient(database='test4')
    client.create_database('test4')

    try:
        first_timestamp = list(client.query("select first(close) from candle",epoch='ms').get_points(measurement='candle'))[0]['time']
    except Exception as e:
        first_timestamp = 0

    if int(argv[1]) < first_timestamp:
        # main(client,1385757000000)
        main(client,first_timestamp)
    else:
        main(client,int(argv[1]))

