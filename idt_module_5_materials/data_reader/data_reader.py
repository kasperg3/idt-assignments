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




from math import pi, sqrt, atan2
import csv
from re import X
from chardet import detect
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

        self.velZ = []

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

    def loadCSV_GPS(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampS.append(TimestampS)
                self.lat.append(float(row['lat']))
                self.lon.append(float(row['lon']))

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
                self.velZ.append(float(row['vz']))


class FailureDetector():
    def __init__(self):
        self.acc_x = []
        self.acc_y = []
        self.acc_z = []
        self.threshold_x = 9.82
        self.threshold_y = 9.82
        self.threshold_z = 5
        self.hasCrashed = False
        self.windowOffset = 0

    def update(self, x, y, z):
        # TODO this will cause memory problems at some point
        self.acc_x.append(x)
        self.acc_y.append(y)
        self.acc_z.append(z)

    def getWindowAverage(self, data, offset, windowSize):
        window = data[offset: offset + windowSize]
        return sum(window) / windowSize

    def getWindowDifference(self, windowSize1, windowSize2):
        return [abs(self.getWindowAverage(self.acc_x, self.windowOffset, windowSize1) - self.getWindowAverage(self.acc_x, self.windowOffset + windowSize1, windowSize2)),
                abs(self.getWindowAverage(self.acc_y, self.windowOffset, windowSize1) - self.getWindowAverage(
                    self.acc_y, self.windowOffset + windowSize1, windowSize2)),
                abs(self.getWindowAverage(self.acc_y, self.windowOffset, windowSize1) - self.getWindowAverage(self.acc_z, self.windowOffset + windowSize1, windowSize2))]

    def isCrashing(self):
        # Do calculations and if true never be false again (latch mechanic)
        result = False
        if self.hasCrashed:
            result = True
        else:
            if len(self.acc_x) > 5:
                # average of second sample period
                diff = self.getWindowDifference(10, 10)
                self.windowOffset = self.windowOffset + 1
                if diff[0] > self.threshold_x or diff[1] > self.threshold_y or diff[2] > self.threshold_z:
                    result = True

        self.hasCrashed = result
        return result


# Class end - Main start
if __name__ == '__main__':
    FILE_NAME = 'TEST5_30-01-19'
    # FILE_NAME = 'TEST8_30-01-19'
    # FILE_NAME = 'TEST9_08-02-19'
    RELATIVE_PATH = 'idt_module_5_materials/csv_files/' + FILE_NAME + '/' + FILE_NAME
    SENSOR_COMBINED = RELATIVE_PATH + '_sensor_combined_0.csv'
    MANUAL_CONTROLLED_SETPOINT = RELATIVE_PATH + '_manual_control_setpoint_0.csv'
    GPS = RELATIVE_PATH + '_vehicle_gps_position_0.csv'
    POSITION = RELATIVE_PATH + '_vehicle_local_position_0.csv'

    # Initialize and load data
    imu = data_loader(SENSOR_COMBINED, debug=True)
    imu.loadCSV_IMU()

    trigger = data_loader(MANUAL_CONTROLLED_SETPOINT, debug=True)
    trigger.loadCSV_para()

    gps = data_loader(GPS, debug=True)
    gps.loadCSV_GPS()

    position = data_loader(POSITION, debug=True)
    position.loadCSV_position()

    # Failure detection
    detector = FailureDetector()

    failure_detection = []
    for i in range(len(imu.AccelerometerXS)):
        detector.update(imu.AccelerometerXS[i],
                        imu.AccelerometerYS[i], imu.AccelerometerZS[i])
        failure_detection.append(int(detector.isCrashing()))

    # Plotting
    fig, (ax, ax1, ax2) = plt.subplots(1, 3)

    # acceleration plot:
    ax_twin = ax.twinx()
    ax.plot(imu.TimestampS, imu.AccelerometerXS,
            linewidth=0.5, label='accel_x')
    ax.plot(imu.TimestampS, imu.AccelerometerYS,
            linewidth=0.5, label='accel_y')
    ax.plot(imu.TimestampS, imu.AccelerometerZS,
            linewidth=0.5, label='accel_z')

    ax_twin.plot(imu.TimestampS, failure_detection,
                 linewidth=1, label='detection')
    # ax.plot(trigger.ParaTimestampS, trigger.ParaTriggerS,
    #         linewidth=1, label='para_trigger')
    ax.set(xlabel='time (s)', ylabel='acceleration (m/s^2)',
           title='Acceleration Plot')
    ax_twin.set_ylabel('Failure')
    ax_twin.set_ylim(-1, 2)
    legend = ax.legend(loc='best', shadow=True, fontsize='medium')
    ax.grid()

    # # gyro plot

    ax1.plot(imu.TimestampS, imu.GyroX,
             linewidth=0.5, label='gyro_x')
    ax1.plot(imu.TimestampS, imu.GyroY,
             linewidth=0.5, label='gyro_y')
    ax1.plot(imu.TimestampS, imu.GyroZ,
             linewidth=0.5, label='gyro_z')
    ax1.plot(imu.TimestampS, failure_detection,
             linewidth=1, label='detection')
    ax1.set(xlabel='time (s)', ylabel='Angular rate',
            title='Gyrometer plot')
    legend = ax1.legend(loc='best', shadow=True, fontsize='medium')
    ax1.grid()

    # Position Plot
    ax2.plot(position.TimestampS, position.positionX, linewidth=0.5, label='x')
    ax2.plot(position.TimestampS, position.positionY, linewidth=0.5, label='y')
    ax2.plot(position.TimestampS, position.positionZ, linewidth=0.5, label='z')
    ax2.plot(position.TimestampS, position.velZ,
             linewidth=1, label='z velocity')

    ax2.set(xlabel='time (s)', ylabel='Z velocity [m/s]', title='Z velocity')
    legend = ax2.legend(loc='best', shadow=True, fontsize='medium')
    ax2.grid()

    plt.show()

# Main end
