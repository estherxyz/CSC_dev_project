#-*-coding:utf-8 -*-
import datetime
import time
import traceback
import requests
from random import *
import json
import sys
import configparser

from influxdb import InfluxDBClient
# import numpy as np
import random

import get_env_variable as env_var  # include define lib for get env variable

"""
post data to influxdb on CF.
measurement: sys.argv[1]


send pair of smartbox, channel data to influxdb with time info.

send data by influxdb python lib.
time record by python.
1 sec, 8192 raw data.
"""



# read config file
config = configparser.ConfigParser()
config.read('config.ini')
host = config['influxdb']['host']
port = config['influxdb']['port']
database = config['influxdb']['database']
username = config['influxdb']['username']
password = config['influxdb']['password']

client = InfluxDBClient(host, port, username, password, database)   # connect influxdb

# obj = env_var.get_influxdb_info()   # get cf environment variable
# client = InfluxDBClient(obj['host'], obj['port'], obj['username'], obj['password'], obj['database'])   # connect influxdb


measurement = str(sys.argv[1])
print('measurement: ' + measurement)

smartbox = ['box1', 'box2']
channel = ['ch1', 'ch2', 'ch3']


time_format = '%Y-%m-%dT%H:%M:%S.%fZ'  # time format
#now_time = datetime.datetime.now() - datetime.timedelta(hours=8)
now_time = datetime.datetime.now()
str_time = now_time.strftime(time_format)   # trans time to string

start_time = now_time   # start_time: compute for 2 mins, now_time: coumpute for fill timestamp


Fs = 8192  # count of data
Ts = 1.0/Fs # 1 second
ff = 5  # frequency of the signal


num = 0
while num<60:    # loop for simulating 2 hours

    # open file
    data = json.load(open('data.txt'))

    start_time = start_time + datetime.timedelta(seconds=1) # simulation 1 second
    now_time = start_time

    num = num + 1
    json_body = []
    print(num)
    print(start_time.strftime(time_format))

#    for item in data['channel'][0:8192]:
    for item in range(8192):
        # now_time = datetime.datetime.now()  # get now time
        now_time = now_time + datetime.timedelta(microseconds=Ts*1000000)   # set time interval
        # print(now_time.strftime(time_format))

        
        # smartbox1, ch1
        json_body.append(
            {
                "measurement": measurement,
                "tags": {
                    "smartbox": smartbox[0],
                    "channel": channel[0]
                },
                "time": now_time.strftime(time_format),
                "fields": {
#                    "value": float(item)
                    "value": float(random.randint(3,10)*5.3)
                }
            }
        )


    client.write_points(json_body)
    print('--- example ---')
    print(json_body[0:5])


