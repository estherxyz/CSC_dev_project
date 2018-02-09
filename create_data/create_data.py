#-*-coding:utf-8 -*-
import datetime
import time
import traceback
import requests
from random import *
# import configparser

from influxdb import InfluxDBClient
import numpy as np

import get_env_variable as env_var  # include define lib for get env variable

"""
post data to influxdb on CF.
measurement: cpu_v1


send pair of smartbox, channel data to influxdb with time info.

send data by influxdb python lib.
time record by python.
send data each 1 second.
"""



# # read config file
# config = configparser.ConfigParser()
# config.read('config.ini')
# host = config['influxdb']['host']
# port = config['influxdb']['port']
# database = config['influxdb']['database']
# username = config['influxdb']['username']
# password = config['influxdb']['password']

# client = InfluxDBClient(host, port, username, password, database)   # connect influxdb

obj = env_var.get_influxdb_info()   # get cf environment variable
client = InfluxDBClient(obj['host'], obj['port'], obj['username'], obj['password'], obj['database'])   # connect influxdb

measurement = 'cpu_v1'  # influxdb measurement name
smartbox = ['box1', 'box2']
channel = ['ch1', 'ch2']
value = [0, 0]


time_format = '%Y-%m-%dT%H:%M:%SZ'  # time format
now_time = datetime.datetime.now() - datetime.timedelta(hours=8)    # push to CF
str_time = now_time.strftime(time_format)   # trans time to string
print(str_time)


Fs = 100.0  # sampling rate
Ts = 1.0/Fs # sampling interval
ff = 5  # frequency of the signal

num = 0
while 1:    # loop

    for t in np.arange(0,1,Ts):
        now_time = datetime.datetime.now()  # get now time
        value[0] = 3 * np.sin(2*np.pi*ff*t)    # amplitude=3
        value[1] = 3 * np.sin(2*np.pi*ff*t) + 2 * np.sin(1*np.pi*ff*t)

        
        # smartbox1, ch1
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "smartbox": smartbox[0],
                    "channel": channel[0]
                },
                "time": now_time.strftime(time_format),
                "fields": {
                    "value": value[0]
                }
            }
        ]
        client.write_points(json_body)  # write data to influxdb

        # smartbox1, ch2
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "smartbox": smartbox[0],
                    "channel": channel[1]
                },
                "time": now_time.strftime(time_format),
                "fields": {
                    "value": value[1]
                }
            }
        ]
        client.write_points(json_body)  # write data to influxdb

        # smartbox2, ch1
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "smartbox": smartbox[1],
                    "channel": channel[0]
                },
                "time": now_time.strftime(time_format),
                "fields": {
                    "value": value[0]
                }
            }
        ]
        client.write_points(json_body)  # write data to influxdb

        # smartbox2, ch2
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "smartbox": smartbox[1],
                    "channel": channel[1]
                },
                "time": now_time.strftime(time_format),
                "fields": {
                    "value": value[1]
                }
            }
        ]
        client.write_points(json_body)  # write data to influxdb


        time.sleep(1)



