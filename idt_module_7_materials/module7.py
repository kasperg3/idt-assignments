#!/usr/bin/env python3
import math
import csv
from ctypes import sizeof
from matplotlib import pyplot as plt
import numpy as np
from pygeodesy import ellipsoidalVincenty, utm
import pandas as pd
from itertools import islice

from polysimplify import VWSimplifier


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


class PathSimplification():
    def __init__(self):
        # TODO move functions into this and create a module for this
        pass


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


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def DouglasPeucker(data, epsilon=0.01, metric='distance'):
    # Minimizes the deviation from the track
    dmax = 0
    angle_min = 3.15
    index = 0
    end = len(data) - 1
    for i in range(len(data)-1):
        p1 = np.array([data[0]['northing'], data[0]['easting']])
        p2 = np.array([data[end]['northing'], data[end]['easting']])
        p3 = np.array([data[i]['northing'], data[i]['easting']])

        # Distance to point
        d = np.linalg.norm(np.cross(p2-p1, p1-p3)) / \
            np.linalg.norm(p2-p1)

        # Minimum angle
        if d > dmax:
            index = i
            dmax = d

        # angle = angle_between(p2-p1, p3-p2)
        # if angle < angle_min:
        #     index = i
        #     angle_min
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
    simplified_path = DouglasPeucker(filtered_data, 1.0)
    plot_coordinates(simplified_path)

    # simplify with number of points using Visvalingam-Whyatt polyline simplification
    test = []
    for d in filtered_data:
        test.append([d['northing'], d['easting']])

    simplifier = VWSimplifier(test)
    VWpts = simplifier.from_ratio(0.05)

    xs = [x[0] for x in VWpts]
    ys = [x[1] for x in VWpts]
    plt.figure(1)
    plt.plot(xs, ys)
    plt.axis('equal')
    plt.show()

    # convert back to lat lon
    # This is already contained in the data
    # Create a mission plan

    # export longitude/latitude
    import exportkml
    kml = exportkml.kmlclass()
    kml.begin('testfile.kml', 'Example', 'Example on the use of kmlclass', 0.7)
    kml.trksegbegin('', '', 'red', 'absolute')
    data_to_write = simplified_path
    for i in range(len(data_to_write)):
        kml.pt(data_to_write[i]['lon'], data_to_write[i]['lat'], 0)
    kml.trksegend()
    kml.end()

    import qgc_plan_generator
    height = 50
    generator = qgc_plan_generator.QGCPlanGenerator()
    generator.set_home_position(
        simplified_path[0]['lon'], simplified_path[0]['lat'], height)

    for d in simplified_path:
        generator.add_waypoint(d['lon'], d['lat'], height)

    generator.generate()


if __name__ == '__main__':
    main()
