#!/usr/bin/env python3
import csv
from matplotlib import pyplot as plt
from pygeodesy import ellipsoidalVincenty, utm
import pandas as pd


class DataLoader:
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


def plot_coordinates(data):
    df = pd.DataFrame(data)
    plt.figure(1)
    plt.plot(df['easting'], df['northing'])
    plt.show()


def filter_outliers():

    return []


def main():

    # load csv file test.csv and convert from Geodetic to UTM
    RELATIVE_PATH = 'idt_module_7_materials/test.csv'
    data_loader = DataLoader(RELATIVE_PATH)
    # print(data_loader.data)
    plot_coordinates(data_loader.data)
    # do outlier detection, based on for example velocity

    # Remove outliers
    # convert back to lat lon
    # Create a mission plan


if __name__ == '__main__':
    main()
