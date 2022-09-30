#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2019-03-27 VKT Version 1.0
"""
"""
Description:
    Simple example python class for loading data from csv files and plotting data.
License: BSD 3-Clause
"""

### Import start
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pow
### Import end

### Class start
class data_loader():
    def __init__(self, inFileName, debug = False):
        self.fileName = inFileName;

        # Prepare containers for the data
        self.TimestampS = []
        self.AccelerometerXS = []
        self.AccelerometerYS = []
        self.AccelerometerZS = []

        self.ParaTimestampS = []
        self.ParaTriggerS = []

        # remember to add class definitions for variables

        # Print debug value
        self.debugText = debug

    def loadCSV_para(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                ParaTimestampS = float(row['timestamp'])/1000000
                self.ParaTimestampS.append(ParaTimestampS)
                ParaTrigger = float(row['aux1']) * 20
                self.ParaTriggerS.append(ParaTrigger)

            if self.debugText:
                print('Data loaded')

    def loadCSV_accel(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampS.append(TimestampS)
                AccelerometerX = float(row['accelerometer_m_s2[0]'])
                self.AccelerometerXS.append(AccelerometerX)
                AccelerometerY = float(row['accelerometer_m_s2[1]'])
                self.AccelerometerYS.append(AccelerometerY)
                AccelerometerZ = float(row['accelerometer_m_s2[2]'])
                self.AccelerometerZS.append(AccelerometerZ)

            if self.debugText:
                print('Data loaded')

    # Extend class with more methods for loading different kind of csv files..
    # e.g loading 'TEST9_08-02-19_telemetry_status_0.csv':
    #
    # loadCSV_telemetry_status(self):
    #    with open(self.fileName) as csvfile:
    #       if self.debugText:
    #           print 'Data file opened, attempting data load'
    #       readCSV = csv.DictReader(csvfile, delimiter=',')
    #       for row in readCSV:
    #       TelemTimestampS = float(row['timestamp'])/1000000
    #       self.TelemTimestampS.append(ParaTimestampS)
    #       RXerrors = float(row['rxerrors'])
    #       self.RXerrorsS.append(RXerrors)
    #
    # (...)




### Class end - Main start

if __name__ == '__main__':

    SENSOR_COMBINED = '../csv_files/TEST9_08-02-19/TEST9_08-02-19_sensor_combined_0.csv'
    MANUAL_CONTROLLED_SETPOINT = '../csv_files/TEST9_08-02-19/TEST9_08-02-19_manual_control_setpoint_0.csv'

    # Initialize and load data
    reader = data_loader(
        SENSOR_COMBINED,
        debug = True
    )
    reader.loadCSV_accel()

    trigger = data_loader(
        MANUAL_CONTROLLED_SETPOINT,
        debug = True
    )
    trigger.loadCSV_para()

    # Add readers for the additional files you want to load...

    # Here you can add the analysis of the different parameters and create boolean variables that triggers upon failure detection.
    # You can likewise plot these failure detection parameters (with the same timestamp as the investigated dataset) together with the logged data.

    fig, ax = plt.subplots()

    # acceleration plot:
    ax.plot(reader.TimestampS, reader.AccelerometerXS, linewidth=0.5, label='accel_x')
    ax.plot(reader.TimestampS, reader.AccelerometerYS, linewidth=0.5, label='accel_y')
    ax.plot(reader.TimestampS, reader.AccelerometerZS, linewidth=0.5, label='accel_z')
    # parachute trigger plot:
    ax.plot(trigger.ParaTimestampS, trigger.ParaTriggerS, linewidth=1, label='para_trigger')

    # Add more plots or create new plots for additional data loaded...

    # plot settings
    ax.set(xlabel='time (s)', ylabel='acceleration (m/s^2)',
       title='Acceleration Plot of Test 9')
    legend = ax.legend(loc='best', shadow=True, fontsize='medium')
    ax.grid()
    
    plt.show()

### Main end
