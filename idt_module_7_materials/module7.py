#!/usr/bin/env python3
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
                                  'heading': float(row['heading'])
                                  })
        self.df = pd.DataFrame(self.data)


def plot_coordinates(data):
    df = data.df
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


def filter_outliers(dl):
    window_size = 5
    filtered_data = []

    for i in range(len(dl.data) - window_size + 1):
        sequence = dl.data[i: i + window_size]
        # remove outliers based on the maximum distance  between two  points
        # relative to  the time  between  recording and  the  maximum speed  of
        # thedrone (in this case your walking speed

    return filtered_data


def path_pruning(dl):
    pass


def main():

    # load csv file test.csv and convert from Geodetic to UTM
    RELATIVE_PATH = 'idt_module_7_materials/rosbag_test.csv'
    data_loader = DataLoader(RELATIVE_PATH)
    # print(data_loader.data)
    plot_coordinates(data_loader)
    # do outlier removal
    filter_outliers(data_loader)
    # implement a path pruning algorithm minimize the points used

    # convert back to lat lon

    # Create a mission plan


if __name__ == '__main__':
    main()
