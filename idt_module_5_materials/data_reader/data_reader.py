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

# Import start
# Import end

# Class start




import csv
from re import X
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pow
class data_loader():
    def __init__(self, inFileName, debug=False):
        self.fileName = inFileName

        # Prepare containers for the data
        # gyro_rad[0],gyro_rad[1],gyro_rad[2],
        # gyro_integral_dt,accelerometer_timestamp_relative,accelerometer_m_s2[0],
        # accelerometer_m_s2[1],accelerometer_m_s2[2],accelerometer_integral_dt
        self.TimestampS = []
        self.AccelerometerXS = []
        self.AccelerometerYS = []
        self.AccelerometerZS = []

        self.GyroX = []
        self.GyroY = []
        self.GyroZ = []

        self.lat = []
        self.lon = []

        self.positionX = []
        self.positionY = []
        self.positionZ = []

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

    def loadCSV_IMU(self):
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
                self.GyroX.append(float(row['gyro_rad[0]']))
                self.GyroY.append(float(row['gyro_rad[1]']))
                self.GyroZ.append(float(row['gyro_rad[2]']))

            if self.debugText:
                print('Data loaded')
                print('Added ', len(self.TimestampS), " rows")

    def loadCSV_GPS(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampS.append(TimestampS)
                # self.lat.append(float(row['lat']))
                # self.lon.append(float(row['lon']))

            if self.debugText:
                print('Data loaded')

    def loadCSV_position(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampS.append(TimestampS)
                self.positionX.append(float(row['x']))
                self.positionY.append(float(row['y']))
                self.positionZ.append(float(row['z']))

            if self.debugText:
                print('Position Data loaded')
                print('Added ', len(self.TimestampS), " rows")


# Class end - Main start
if __name__ == '__main__':

    SENSOR_COMBINED = 'idt_module_5_materials/csv_files/TEST9_08-02-19/TEST9_08-02-19_sensor_combined_0.csv'
    MANUAL_CONTROLLED_SETPOINT = 'idt_module_5_materials/csv_files/TEST9_08-02-19/TEST9_08-02-19_manual_control_setpoint_0.csv'
    GPS = 'idt_module_5_materials/csv_files/TEST9_08-02-19/TEST9_08-02-19_vehicle_gps_position_0.csv'
    POSITION = 'idt_module_5_materials/csv_files/TEST9_08-02-19/TEST9_08-02-19_vehicle_local_position_0.csv'

    # Initialize and load data
    reader = data_loader(SENSOR_COMBINED, debug=True)
    reader.loadCSV_IMU()

    trigger = data_loader(MANUAL_CONTROLLED_SETPOINT, debug=True)
    trigger.loadCSV_para()

    gps = data_loader(GPS, debug=True)
    gps.loadCSV_GPS()

    position = data_loader(POSITION, debug=True)
    position.loadCSV_position()

    # Add readers for the additional files you want to load...

    # Here you can add the analysis of the different parameters and create boolean variables that triggers upon failure detection.
    # You can likewise plot these failure detection parameters (with the same timestamp as the investigated dataset) together with the logged data.

    fig, (ax, ax1, ax2) = plt.subplots(1, 3)

    # acceleration plot:
    ax.plot(reader.TimestampS, reader.AccelerometerXS,
            linewidth=0.5, label='accel_x')
    ax.plot(reader.TimestampS, reader.AccelerometerYS,
            linewidth=0.5, label='accel_y')
    ax.plot(reader.TimestampS, reader.AccelerometerZS,
            linewidth=0.5, label='accel_z')
    ax.set(xlabel='time (s)', ylabel='acceleration (m/s^2)',
           title='Acceleration Plot')
    legend = ax.legend(loc='best', shadow=True, fontsize='medium')
    ax.plot(trigger.ParaTimestampS, trigger.ParaTriggerS,
            linewidth=1, label='para_trigger')
    ax.grid()

    # gyro plot
    ax1.plot(reader.TimestampS, reader.GyroX,
             linewidth=0.5, label='gyro_x')
    ax1.plot(reader.TimestampS, reader.GyroY,
             linewidth=0.5, label='gyro_y')
    ax1.plot(reader.TimestampS, reader.GyroZ,
             linewidth=0.5, label='gyro_z')
    ax1.set(xlabel='time (s)', ylabel='Angular rate',
            title='Gyrometer plot')
    legend = ax1.legend(loc='best', shadow=True, fontsize='medium')
    ax1.grid()

    # GPS / Velocity plot

    # Position
    ax2.plot(position.TimestampS, position.positionX, linewidth=0.5, label='x')
    ax2.plot(position.TimestampS, position.positionY, linewidth=0.5, label='y')
    ax2.plot(position.TimestampS, position.positionZ, linewidth=0.5, label='z')
    ax2.set(xlabel='time (s)', ylabel='local position [m]', title='Position')
    legend = ax2.legend(loc='best', shadow=True, fontsize='medium')
    ax2.grid()

    plt.show()

# Main end
