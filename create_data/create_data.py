#-*-coding:utf-8 -*-
import datetime
import time
import traceback
import requests
from random import *
import json
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
2 mins, 80000 raw data.
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

measurement = 'cpu_v1'
smartbox = ['box1', 'box2']
channel = ['ch1', 'ch2', 'ch3']


time_format = '%Y-%m-%dT%H:%M:%S.%fZ'  # time format
now_time = datetime.datetime.now() - datetime.timedelta(hours=8)    # push to CF
str_time = now_time.strftime(time_format)   # trans time to string

start_time = now_time   # start_time: compute for 2 mins, now_time: coumpute for fill timestamp


Fs = 80000  # count of data
Ts = 120.0/Fs # 2 mins
ff = 5  # frequency of the signal


num = 0
while num<60:    # loop for simulating 2 hours

    # open file
    data = json.load(open('data.txt'))

    start_time = start_time + datetime.timedelta(minutes=2) # simulation 2 mins
    now_time = start_time

    num = num + 1
    json_body = []
    # print(num)

    for item in data['channel']:
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
                    "value": float(item)
                }
            }
        )


    client.write_points(json_body)

