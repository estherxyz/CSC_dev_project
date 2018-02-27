#-*-coding:utf-8 -*-
import datetime
import time
import json
import traceback
import re



def get_param_list(str_param):
    """
    parse request body to param list from grafana simple json.

    @param str_param: (string) grafana simple json request param.
    @return req_param: (dict) return dict for param list
    """
    req_param = {}  # trans param in dict


    str_param = str_param.split(',')  # split param string to list
    
    # split each key, value pair
    for item in str_param:
        item = item.split('=')  # split string to  key, value by =
        
        key = item[0]
        value = re.split('[\|\(\)]', item[1])  # split |()

        if (len(value)>=3):
            value = value[1:-1]   # remove first and last

        # empty string, pass
        if (len(value)<=1) and (value[0]==''):
            continue

        # print(value_list)
        req_param[key] = value    # add to dict

    
    return req_param



def get_param_constraint(req_param):
    """
    trans pair of param(key, value) to query constraint.

    @param  req_param: (dict) pair of param(key, value list)
    @return query_list: (list) trans to query constraint string list
    """
    query_list = []
    count = 0

    for key, value in req_param.items():
        if key == '_type':
            continue
        if key == 'measurement':
            continue
            

        str_query = '('
        count = 0

        for item in value:
            count = count + 1
            str_query = str_query + str(key) + '=\'' + str(item) + '\''
            
            if count != len(value):
                str_query = str_query + ' OR '
            else:
                str_query = str_query + ')'
        
        query_list.append(str_query)


    return query_list



def combine_constraint(query_list):
    """
    combine query list to query constraint string.

    @param  query_list: (list) each param pair trans to query list.
    @return query_constraint: (string) combine query list to query string.
    """
    query_constraint = ''

    if len(query_list)!=0:
        query_constraint = '('  # string for combine query list
        count = 0

        for item in query_list:
            count = count + 1
            query_constraint = query_constraint + item

            if count != len(query_list):
                query_constraint = query_constraint + ' AND '
            else:
                query_constraint = query_constraint + ')'


    return query_constraint



def trans_time_value(str_time):
    """
    trans time string to another format.

    @param  str_time: (string) origin time value: %Y-%m-%dT%H:%M:%S.000Z
    @return result: (string) format: %Y-%m-%dT%H:%M:%SZ
    """
    time_format = '%Y-%m-%dT%H:%M:%SZ'

    result = str_time.split('.')
    result = result[0] + 'Z'

    return result



def get_query_string(measurement, query_constraint, time_start, time_end):
    """
    get query string for influxdb.

    @param  measurement: (string) measurement name in influxdb.
    @param  query_constraint: (string) param for query string.
    @param  time_start: (string) query time range for start.
    @param  time_end: (string) query time range for end.
    @return query: (string) query string for influxdb.
    """
    query_from = "select value from " + measurement + " where "
    query_limit = ' limit 40000'    # limit of raw data
    query_time = " (time>='" + time_start + "' AND time<='" + time_end + "') "  # time range
    

    # combine query string
    query = query_from + query_time
    if query_constraint != '':
        query =  query + ' AND ' + query_constraint
    
    query = query + query_limit


    return query

