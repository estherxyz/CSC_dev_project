#-*-coding:utf-8 -*-
import traceback
import json
import os

from influxdb import InfluxDBClient

"""
get env variable on cf.
"""



def get_service_name():
    """
    get service name of cf environment variables.

    @return service_name: (string) sercice name on CF
    """
    service_name = str(os.getenv('SERVICE_NAME'))

    return service_name



def get_influxdb_info():
    """
    get influxdb credential infomation of cf environment variables.

    @return credential_obj: (dict) dictionary for database info
                            {host, port, database, username, password, uri}
    """
    if 'VCAP_SERVICES' in os.environ:
        # get VCAP_SERVICES
        vcap_services = json.loads(os.environ['VCAP_SERVICES'])

        # get service name of influxdb
        service_name = get_service_name()

        # get service info
        service_obj = vcap_services[service_name][0]
        credential_obj = service_obj['credentials']

        return credential_obj
    
    else:
        return {}


