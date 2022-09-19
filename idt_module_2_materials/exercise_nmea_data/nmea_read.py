#!/usr/bin/env python3
# /****************************************************************************
# nmea read function
# Copyright (c) 2018-2020, Kjeld Jensen <kj@kjen.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ****************************************************************************/
'''
2018-03-13 Kjeld First version, that reads in CSV data
2020-02-03 Kjeld Python 3 compatible
2020-09-17 Kjeld Changed first line to python3
'''
import os
import numpy as np


class nmea_line:
    # Class for parsing a NMEA 0183 line
    def __init__(self, line):
        self.line = line.split(',')  # split into comma separated list
        # https://www.gpsworld.com/what-exactly-is-gps-nmea-data/
        # The $GPGGA is a basic GPS NMEA message. There are alternative and companion NMEA messages that provide similar or additional information.
        # self.columns = ["talker_type", "utc_time", "lattitude", "lattitude_direction", "longitude", "longitude_direction", "quality", "n_sattelites","hdop","antenna_altitude", "altitude_unit", "geoidal_separation","correction_age","correction_station_id","checksum"]
        # self.talker_type = self.__getColumnValue(0,line)
        # #$GPGSA – Detailed GPS DOP and detailed satellite tracking information (eg. individual satellite numbers). $GNGSA for GNSS receivers.
        # #$GPGSV – Detailed GPS satellite information such as azimuth and elevation of each satellite being tracked. $GNGSV for GNSS receivers.
        # #$GPVTG – Speed over ground and tracking offset.
        # #$GPGST – Estimated horizontal and vertical precision. $GNGST for GNSS receivers.
        # self.utc_time = self.__getColumnValue(1,line)
        # self.lattitude = self.__getColumnValue(2,line) # DDMM.MMMMM format
        # self.lattitude_direction = self.__getColumnValue(3,line) # N or S
        # self.longitude = self.__getColumnValue(4,line) # DDMM.MMMMM format
        # self.longitude_direction = self.__getColumnValue(5,line) # W or E
        # self.quality = self.__getColumnValue(6,line) # 1= uncorrected coordinate,
        # #2 = Differentially correct coordinate (e.g., WAAS, DGPS)
        # #4 = RTK Fix coordinate (centimeter precision)
        # #5 = RTK Float (decimeter precision.
        # self.n_sattelites = self.__getColumnValue(7,line)
        # self.hdop = self.__getColumnValue(8,line) # horizontal dilution precision
        # self.antenna_altitude = self.__getColumnValue(9,line)
        # self.altitude_unit = self.__getColumnValue(10,line)
        # self.geoidal_separation = self.__getColumnValue(11,line) # geoidal separation (subtract this from the altitude of the antenna to arrive at the Height Above Ellipsoid (HAE).
        # self.geoidal_unit = self.__getColumnValue(12,line)
        # self.correction_age = self.__getColumnValue(13,line)
        # self.correction_station_id = self.__getColumnValue(14,line)
        # #self.checksum = self.__getColumnValue(15,line) TODO make this work, currently the checksum is a part of the station id

    # def __getColumnValue(self,index, line):
    #   result = ""
    #   try:
    #     result = line[index]
    #   except Exception as e:
    #     print(e)
    #   return result
    def getNmeaMsg(self):
        return self.msg

    def getColumnData(self, index):
        return self.line[index]

    def print(self):
        print(self.line)


class nmea_class:
    def __init__(self):
        self.data = []

    def import_file(self, file_name):
        file_ok = True
        try:
            # read all lines from the file and strip \n
            lines = [line.rstrip() for line in open(file_name)]
        except Exception as e:
            file_ok = False
            print(e)
        if file_ok == True:
            pt_num = 0
            for i in range(len(lines)):  # for all lines
                if len(lines[i]) > 0 and lines[i][0] != '#':  # if not a comment or empty line
                    self.data.append(nmea_line(lines[i]))

    def getColumnData(self, index):
        result = []
        row: nmea_line
        for row in self.data:
            result.append(row.getColumnData(index))
        return result

    def print_data(self):
        for row in self.data:
            row.print()


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import exportkml
    import math
    print('Importing nmea_trimble_gnss_eduquad_flight.txt')
    nmea = nmea_class()
    nmea.import_file('nmea_trimble_gnss_eduquad_flight.txt')
    # nmea.import_file ('nmea_ublox_neo_24h_static.txt')

    time = np.array(nmea.getColumnData(1)).astype(float)
    antenna_altitude = np.array(nmea.getColumnData(9)).astype(float)
    # 11   = Geoidal separation (Diff. between WGS-84 earth ellipsoid and mean sea level.  -=geoid is below WGS-84 ellipsoid)
    geoidal_separation = np.array(nmea.getColumnData(11)).astype(float)
    unit_antenna = np.array(nmea.getColumnData(10))
    unit_geoidal = np.array(nmea.getColumnData(12))
    hae = antenna_altitude

    # Long lat DDMM.MMMMM format
    lattitude = np.array(nmea.getColumnData(2)).astype(float)
    longitude = np.array(nmea.getColumnData(4)).astype(float)

    # Convert to DDDD.MMMMM
    for i in range(len(lattitude)):
        deg = math.floor(lattitude[i]/100.)  # DD
        min = (lattitude[i] % 100.) / 60.  # MMMMM
        lattitude[i] = deg + min

    for i in range(len(longitude)):
        deg = math.floor(longitude[i]/100.)
        min = (longitude[i] % 100.) / 60.
        longitude[i] = deg + min

    # export longitude/latitude
    kml = exportkml.kmlclass()
    kml.begin('testfile.kml', 'Example', 'Example on the use of kmlclass', 0.7)
    kml.trksegbegin('', '', 'red', 'absolute')
    for i in range(len(lattitude)):
        kml.pt(lattitude[i], longitude[i], 0)
    kml.trksegend()
    kml.end()

    # Get the number of sattelites
    n_sattelites = np.array(nmea.getColumnData(7)).astype(int)

    nmea = nmea_class()
    print("Importing nmea_ublox_neo_24h_static.txt")
    nmea.import_file('nmea_ublox_neo_24h_static.txt')
    # http://aprs.gids.nl/nmea/#gsa
    gdop = []
    gdop_time = []
    temp = 0

    for row in nmea.data:
        if row.line[0] == "$GPGGA":
            temp = float(row.line[1])

        if row.line[0] == "$GPGSA":
            # row.line[14] # PDOP
            hdop = float(row.line[15])  # HDOP
            vdop = float(row.line[16])  # VDOP
            # GDOP
            gdop_time.append(temp)
            gdop.append(math.sqrt(hdop**2 + vdop**2))

    print("Plotting...")
    showPlot = False
    if showPlot == True:
        # 1.  Altitude above Mean Sea Level with respect to time during the drone flight.
        plt.figure(1)
        plt.xlabel("Time UTC")
        plt.ylabel("Antenna altitude above/below mean sea level")
        plt.plot(time, hae)
        plt.savefig('height_above_mean_sea_level.png')

        # 2.  Number of satellites tracked with respect to time during the drone flight.
        plt.figure(2)
        plt.xlabel("Time UTC")
        plt.ylabel("number of sattelites")
        plt.plot(time, n_sattelites)
        plt.savefig('number_of_sattelites.png')

        # 3.  Map showing the drone track during the drone flight.
        plt.figure(3)
        plt.title("Drone trajectory")
        plt.xlabel("Longitude")
        plt.ylabel("Lattitude")
        plt.plot(longitude, lattitude, marker=" ")
        plt.savefig('drone_trajectory.png')

        # 4.  Plot showing static GNSS accuracy over 24 hours.
        plt.figure(4)
        plt.title("GDOP")
        plt.xlabel("Time UTC")
        plt.ylabel("GDOP")
        plt.plot(gdop_time, gdop)
        plt.savefig('gdop_precision.png')

        plt.show()
    # 5.  Signal to Noise Ratio (SNR) for the satellites in view with respect to time over 24 hours. (optional)
    # 6.  A hemisphere map of the location of the satellites simulated over time over 24 hours (optional)
