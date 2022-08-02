import datetime
import json
import re
import time


def getTimeStamp(date):
    result = re.search(r"[\-\+]\d+", date)
    if result:
        time_area = result.group()
        symbol = time_area[0]
        offset = int(time_area[1]) + int(time_area[2])
        if symbol == "+":
            format_str = '%a, %d %b %Y %H:%M:%S ' + time_area
            if "UTC" in date:
                format_str = '%a, %d %b %Y %H:%M:%S ' + time_area + ' (UTC)'
            if "GMT" in date:
                format_str = '%a, %d %b %Y %H:%M:%S ' + time_area + ' (GMT)'
            if "CST" in date:
                format_str = '%a, %d %b %Y %H:%M:%S ' + time_area + ' (CST)'
            utcdatetime = time.strptime(date, format_str)
            tempsTime = time.mktime(utcdatetime)
            tempsTime = datetime.datetime.fromtimestamp(tempsTime)
            if offset > 8:
                offset = offset - 8
                tempsTime = tempsTime + datetime.timedelta(hours=offset)
                localtimestamp = tempsTime.strftime("%Y-%m-%d")
            else:
                format_str = '%a, %d %b %Y %H:%M:%S ' + time_area
                utcdatetime = time.strptime(date, format_str)
                tempsTime = time.mktime(utcdatetime)
                tempsTime = datetime.datetime.fromtimestamp(tempsTime)
                tempsTime = tempsTime + datetime.timedelta(hours=(offset + 8))
                localtimestamp = tempsTime.strftime("%Y-%m-%d")
            return localtimestamp


def date2time(date_str=None, time_str=None):
    if date_str:
        time_struct = time.strptime(date_str, "%Y-%m-%d")
    if time_str:
        time_struct = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    time_stamp = time.mktime(time_struct)
    return time_stamp
