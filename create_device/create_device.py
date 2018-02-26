#-*-coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import datetime
import time
import traceback
# import configparser

from influxdb import InfluxDBClient

import get_env_variable as env_var  # include define lib for get env variable

"""
post data to influxdb on cF.
measurement: device_list


send pair of smartbox, channel data to influxdb.

send data by influxdb python lib.
send data each 1 second.
"""


app = Flask(__name__)


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

# measurement = 'device_list'  # influxdb measurement name



@app.route("/device_list/create", methods=['GET'])
def create_device_data():
    """
    create device meta data in influxdb.

    @param  smartbox: smartbox number for meta data
    @param  channel: channel number for meta data
    @param  label: show description of smartbox, channel
    """
    measurement = 'device_list' # influxdb measurement name

    smartbox = request.args.get('smartbox', default = '', type = str)
    channel = request.args.get('channel', default = '', type = str)
    label = request.args.get('label', default = '', type = str)
    

    if (smartbox=='') or (channel=='') or (label==''):
        return jsonify({'msg': 'lose param'})


    # add smartbox, channel
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "smartbox": smartbox,
                "channel": channel,
                "label": label
            },
            "fields": {
                "value": 0
            }
        }
    ]
    client.write_points(json_body)  # write data to influxdb


    return jsonify({'msg': 'success'}), 200



@app.route("/delete_all/<mea_name>", methods=['POST'])
def delete_device_list(mea_name):
    """
    delete device meta data in influxdb.
    """
    # delete measurement: mea_name
    client.delete_series(measurement=mea_name)


    return jsonify({'msg': 'success'}), 200





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    # Careful with the debug mode..

