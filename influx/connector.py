import time
import datetime
import pytz
from influxdb import InfluxDBClient
from utility import _utc_timestamp


def create_record(client: InfluxDBClient, 
                    json_body:list):
    try:
        client.write_points(json_body)
    except Exception as e:
        print(e)


def check_point_existance(client:InfluxDBClient,time_stamp: int, series_name: str):
    result = client.query("SELECT * FROM {} WHERE time = '{}';".format(series_name,_utc_timestamp(time_stamp)))
    return len(list(result.get_points(measurement=series_name)))



if __name__ == "__main__":
    client = InfluxDBClient(database='test4')
    # client.create_database('test1')
    
    # create_record(client, "cpu_load_short", {"host": "server01", "region": "us-west"},1565773132119,{"value": 0.32})

    # print(check_point_existance(client,time_stamp="2013-12-01T05:12:00+00:00", series_name="candle"))


    # result = list(client.query("select first(close) from candle").get_points(measurement='candle'))[0]['time']
    # print(list(result.get_points(measurement='candle'))[:10])
    # print(result)
    print(list(client.query("select * from candle order by time").get_points(measurement='candle'))[:10])
