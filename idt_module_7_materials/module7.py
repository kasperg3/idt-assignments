#!/usr/bin/env python3
import math
import csv
from ctypes import sizeof
from matplotlib import pyplot as plt
import numpy
from pygeodesy import ellipsoidalVincenty, utm
import pandas as pd
from itertools import islice


class DataLoader():
    def __init__(self, inFileName, debug=False):
        self.fileName = inFileName
        self.data = []

        with open(self.fileName) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            for row in readCSV:
                lon = float(row['lon'])
                lat = float(row['lat'])
                ll = ellipsoidalVincenty.LatLon(lat, lon)
                coord = ll.toUtm()
                # TODO add time
                self.data.append({'lon': lon,
                                 'lat': lat,
                                  'alt': float(row['alt']),
                                  'easting': coord.easting,
                                  'northing': coord.northing,
                                  'zone': coord.zone,
                                  'hemisphere': coord.hemisphere,
                                  'rel_alt': float(row['rel_alt']),
                                  'heading': float(row['heading']),
                                  'time': float(row['time'])
                                  })
        self.df = pd.DataFrame(self.data)


def plot_coordinates(data):
    df = pd.DataFrame(data)
    plt.figure(1)
    plt.plot(df['northing'], df['easting'])
    plt.axis('equal')
    plt.show()


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


# Methods max_dist, max_speed, and statistical
def filter_outliers(dl, max_speed):
    filtered_data = []
    # if method == 'statistical':
    #     window_size = 30
    #     for i in range(len(dl.data) - window_size + 1):
    #         sequence = pd.DataFrame(dl.data[i: i + window_size])
    #         easting_z_score = (dl.data[i]['easting'] - sequence['easting'].mean()) / sequence['easting'].std()
    #         northing_z_score = (dl.data[i]['northing'] - sequence['northing'].mean()) / sequence['northing'].std()

    #         # remove outliers based on the z score
    #         if abs(easting_z_score) < 1 or abs(northing_z_score) < 1 :
    #             filtered_data.append(dl.data[i])
    # elif method == 'max_speed':
    for i in range(len(dl.data) - 1):
        pos_change = math.sqrt((dl.data[i]['easting'] - dl.data[i+1]['easting'])**2 + (
            dl.data[i]['northing'] - dl.data[i+1]['northing'])**2)
        time_diff = abs(dl.data[i]['time'] - dl.data[i+1]
                        ['time'])  # Micro to seconds
        if time_diff != 0.0:
            speed = pos_change/(time_diff*0.000001)
            if (speed < max_speed):
                filtered_data.append(dl.data[i])

    return filtered_data


def DouglasPeucker(data, epsilon=0.01):
    # function DouglasPeucker(PointList[], epsilon)
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    end = len(data) - 1
    for i in range(len(data)-1):
        p1 = numpy.array([data[0]['northing'], data[0]['easting']])
        p2 = numpy.array([data[end]['northing'], data[end]['easting']])
        p3 = numpy.array([data[i]['northing'], data[i]['easting']])
        d = numpy.linalg.norm(numpy.cross(p2-p1, p1-p3)) / \
            numpy.linalg.norm(p2-p1)
        if d > dmax:
            index = i
            dmax = d
    result_list = []

    # # If max distance is greater than epsilon, recursively simplify
    if (dmax > epsilon):
        # Recursive call
        recResults1 = DouglasPeucker(data[0:index], epsilon)
        recResults2 = DouglasPeucker(data[index:end], epsilon)

        # Build the result list
        result_list = recResults1 + recResults2
    else:
        result_list = [data[0], data[end]]
    return result_list


def main():
    # load csv file test.csv and convert from Geodetic to UTM
    RELATIVE_PATH = 'idt_module_7_materials/rosbag_test.csv'
    data_loader = DataLoader(RELATIVE_PATH)
    # print(data_loader.data)
    plot_coordinates(data_loader.data)
    # do outlier removal
    filtered_data = filter_outliers(data_loader, 5.0)
    plot_coordinates(filtered_data)
    # implement a path pruning algorithm minimize the points used
    plot_coordinates(DouglasPeucker(filtered_data, 1.0))
    # convert back to lat lon
    # This is already contained in the data
    # Create a mission plan


if __name__ == '__main__':
    main()
