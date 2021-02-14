#!/usr/bin/env python
from prometheus_client import Gauge, start_http_server, Summary
import random
import time
import re

from CO2Meter import *

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
CO2_TEMP = Gauge('co2_temp', 'Temperature in celsius provided by co2 monitor')
CO2_PPM = Gauge('co2_ppm', 'co2 part per million provided by co2 monitor')   

Meter = CO2Meter("/dev/hidraw0")

def read_sensor_co2():
    co2 = Meter.get_co2()
    co2 = co2.get('co2')
    
    if co2 is None:
        return

    CO2_PPM.set(co2)

def read_sensor_temp():
    temp = Meter.get_temperature()
    temp = temp.get('temperature')
    
    if temp is None:
        return

    CO2_TEMP.set(temp)


def main():
    start_http_server(8001)

    while True:
        read_sensor_co2()
        read_sensor_temp()
        time.sleep(5)

main()
