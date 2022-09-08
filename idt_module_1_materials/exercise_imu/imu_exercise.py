#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2020 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

##### Insert initialize code below ###################

## Uncomment the file to read ##
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
# fileName = 'imu_razor_data_static.txt'
fileName = 'imu_razor_data_pitch_55deg.txt'
# fileName = 'imu_razor_data_roll_65deg.txt'
# fileName = 'imu_razor_data_yaw_90deg.txt'

# IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

## Variables for plotting ##
showPlot = True
plotData = []

## Initialize your variables here ##
myValue = 0.0


######################################################

# import libraries

# open the imu data file
f = open(fileName, "r")

# initialize variables
count = 0

# looping through file

y = 0
relative_angle = 0  # pi/2
bias = 0
for line in f:
    count += 1

    # split the line into CSV formatted data
    line = line.replace('*', ',')  # make the checkum another csv value
    csv = line.split(',')

    # keep track of the timestamps
    ts_recv = float(csv[0])
    if count == 1:
        ts_now = ts_recv  # only the first time
    ts_prev = ts_now
    ts_now = ts_recv

    if imuType == 'sparkfun_razor':
        # import data from a SparkFun Razor IMU (SDU firmware)
        acc_x = int(csv[2]) / 1000.0 * 4 * 9.82
        acc_y = int(csv[3]) / 1000.0 * 4 * 9.82
        acc_z = int(csv[4]) / 1000.0 * 4 * 9.82
        gyro_x = int(csv[5]) * 1/14.375 * pi/180.0
        gyro_y = int(csv[6]) * 1/14.375 * pi/180.0
        gyro_z = int(csv[7]) * 1/14.375 * pi/180.0

    elif imuType == 'vectornav_vn100':
        # import data from a VectorNav VN-100 configured to output $VNQMR
        acc_x = float(csv[9])
        acc_y = float(csv[10])
        acc_z = float(csv[11])
        gyro_x = float(csv[12])
        gyro_y = float(csv[13])
        gyro_z = float(csv[14])

    ##### Insert loop code below #########################

    # Variables available
    # ----------------------------------------------------
    # count		Current number of updates
    # ts_prev	Time stamp at the previous update
    # ts_now	Time stamp at this update
    # acc_x		Acceleration measured along the x axis
    # acc_y		Acceleration measured along the y axis
    # acc_z		Acceleration measured along the z axis
    # gyro_x	Angular velocity measured about the x axis
    # gyro_y	Angular velocity measured about the y axis
    # gyro_z	Angular velocity measured about the z axis

    ## Insert your code here ##

    # Exersice 3.2
    roll = atan2(acc_x, sqrt(pow(acc_y, 2.0) + pow(acc_z, 2.0)))
    pitch = atan2(-acc_y, acc_z)

    myValue = pitch  # relevant for the first exercise, then change this.

    if (y == 0):
        y = myValue
    a = 0.2
    y = a*myValue + (1-a)*y
    filtered = y

    # Exersice 3.3: relative angle
    dt = (ts_now-ts_prev)
    bias = 2.5/1000
    relative_angle += (gyro_z - bias) * dt

    # in order to show a plot use this function to append your value to a list:
    # plotData.append(roll*180.0/pi)  # Exersize 3.2.1
    # plotData.append(roll*180.0/pi)  # Exersize 3.2.2
    plotData.append(filtered*180.0/pi)  # Exersize 3.2.4
    # plotData.append(relative_angle*180.0/pi)  # Exersize 3.2.5
    # Exersize 3.2.5 (Use atan2 this method is taking care of limited euler angles)

    ######################################################

# closing the file
f.close()

# show the plot
if showPlot == True:
    plt.plot(plotData)
    ax = plt.gca()
    plt.savefig('imu_exercise_plot_exersice_pitch_filtered3.3.png')
    plt.show()
