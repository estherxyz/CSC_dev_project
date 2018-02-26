#-*-coding:utf-8 -*-
# For flask implementation
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import datetime
import time
import json
import traceback
import requests
import re
# import configparser


import numpy as np
from scipy import signal

from influxdb import InfluxDBClient

import osc_grafana as osc  # include define lib for osc in grafana
import get_env_variable as env_var  # include define lib for get env variable

"""
Get data from influxdb to compute.
measurement: cpu_v1


api compute for wave transform.
request from grafana.
return data for grafana panel.
"""



app = Flask(__name__)


### set connect ###

# # read config file
# config = configparser.ConfigParser()
# config.read('config.ini')
# host = config['influxdb']['host']
# port = config['influxdb']['port']
# database = config['influxdb']['database']
# username = config['influxdb']['username']
# password = config['influxdb']['password']

# client = InfluxDBClient(host, port, username, password, database)   # connect influxdb


# get cf environment variable
obj = env_var.get_influxdb_info()   # get cf environment variable
client = InfluxDBClient(obj['host'], obj['port'], obj['username'], obj['password'], obj['database'])   # connect influxdb


# measurement = 'cpu_v1'

###  ###



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # response.headers['Content-Type'] = 'application/json'

    return response



@app.route("/", methods=['GET','POST'])
def test_1():
    """
    for simple json.
    official page: should return 200 ok. Used for "Test connection" on the datasource config page.
    """
    str_msg = 'test simple json with /'

    return jsonify({'msg': str_msg}), 200



@app.route("/annotations", methods=['GET','POST'])
def test_2():
    """
    for simple json
    """
    str_msg = 'test simple json with /annotations'

    return jsonify({'msg': str_msg}), 200



@app.route("/search", methods=['GET','POST'])
def test_3():
    """
    for simple json
    
    controller for firehose write in this function.
    """
    str_msg = 'test simple json with /search'

    return jsonify({'msg': str_msg}), 200



@app.route("/query", methods=['GET','POST'])
def test_4():
    """
    for simple json (return type: (json) time series)

    plotly simple json osc api write in this function.
    """
    obj_req = request.get_json(silent=True)	# get post json
    if obj_req == None:
        return jsonify({
            'EXEC_DESC': '62',
            'message': 'request body is wrong'
        }), 400


    req_param = osc.get_param_list(obj_req['targets'][0]['target']) # (dict) parse request param

    # check '_type' is exist
    if ('_type' not in req_param) or ('measurement' not in req_param) :
        return jsonify({
            'EXEC_DESC': '61',
            'message': 'lose wave transformation method.'
        }), 400


    query_list = osc.get_param_constraint(req_param)    # (list) transform key, value to constraint string
    query_constraint = osc.combine_constraint(query_list)   # (string) AND constraing list

    time_start = osc.trans_time_value(obj_req['range']['from']) # start time
    time_end = osc.trans_time_value(obj_req['range']['to']) # end time

    measurement = req_param['measurement'][0]
    print ("measurement: " + measurement)
    query = osc.get_query_string(measurement, query_constraint, time_start, time_end)    # get query string
    print("Query string: " + query)


    # route to different osc api
    if req_param['_type'][0] == 'fft':
        resp = osc_fft(query)
    elif req_param['_type'][0] == 'envelope':
        resp = osc_envelope(query)
    else:
        resp = []


    print('/query')
    return jsonify(resp), 200



def osc_fft(query):
    """
    wave transform: fft

    @param  query: (string) query string for influxdb.
    @return resp: (list) fft trans result in grafana timeseries format.
    """
    # grafana simple json response format
    target_name = 'Amplitude'
    resp = []
    resp_item = {
        'target': target_name,
        'datapoints': []    # data
    }


    result = client.query(query)    # query influxdb
    result = result.raw # trans query result to json


    x = []
    if 'series' in result:
        items = result['series'][0]['values']   # data array with data in influxdb
        
        for item in items:
            x.append(item[1])
    
    client.close()


    if len(x) != 0:
        # Compute and plot the spectrogram.
        Fs = 60.0  # rate
        Ts = 1.0/Fs # interval
        ff = 5  # frequency of the signal

        n = len(x) # length of the signal
        k = np.arange(n)
        T = n/Fs
        frq = k/T # two sides frequency range
        frq = frq[range(int(n/2))] # one side frequency ralsge
        Y = np.fft.fft(x)/n # fft computing and normalization
        Y = Y[range(int(n/2))]


        fft = []
        for i in range(int(n/2)):
            fft.append([float(abs(Y[i])), float(frq[i])])

        resp_item['datapoints'] = fft
        resp.append(resp_item)
    
    else:
        resp_item['datapoints'] = []


    return resp



def osc_envelope(query):
    """
    wave transform: envelope (temp)

    @param  query: (string) query string for influxdb.
    @return resp: (list) fft trans result in grafana timeseries format.
    """
    # grafana simple json response format
    target_name = 'envelope test'
    resp = []
    resp_item = {
        'target': target_name,
        'datapoints': []    # data
    }


    result = client.query(query)    # query influxdb
    result = result.raw # trans query result to json


    x = []
    if 'series' in result:
        items = result['series'][0]['values']   # data array with data in influxdb
        
        for item in items:
            x.append(item[1])
    
    client.close()


    if len(x) != 0:
        # Compute and plot the spectrogram.
        Fs = 60.0  # rate
        Ts = 1.0/Fs # interval
        ff = 5  # frequency of the signal

        n = len(x) # length of the signal
        k = np.arange(n)
        T = n/Fs
        frq = k/T # two sides frequency range
        frq = frq[range(int(n/2))] # one side frequency ralsge
        Y = np.fft.fft(x)/n # fft computing and normalization
        Y = Y[range(int(n/2))]


        envelope = []
        for i in range(int(n/2)):
            envelope.append([-(float(abs(Y[i]))), float(frq[i])])

        resp_item['datapoints'] = envelope
        resp.append(resp_item)
    
    else:
        resp_item['datapoints'] = []


    return resp




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=5500, debug=True)
    
    # Careful with the debug mode..

