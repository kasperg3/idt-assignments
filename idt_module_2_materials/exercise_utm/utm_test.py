#!/usr/bin/env python3
#*****************************************************************************
# UTM projection conversion test
# Copyright (c) 2013-2020, Kjeld Jensen <kjeld@frobomind.org>
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
#*****************************************************************************
"""
This file contains a simple Python script to test the UTM conversion class.

Revision
2013-04-05 KJ First version
2015-03-09 KJ Minor update of the license text.
2016-01-16 KJ Corrected a minor problem with the library location reference.
2020-02-03 KJ Python 3 compatible, changed functionality: it now moves a
              geodetic position 100 meter East
2020-09-17 KJ Changed first line to python3
"""

# import utmconv class
from utm import utmconv
from math import pi, cos, sin, sqrt, asin, acos

def getLattitudeConvertionError(lattitude, longitude, lattitude_difference) : 
    (hemisphere, zone, letter, e, n) = uc.geodetic_to_utm (lattitude,longitude)
    e_new = e + lattitude_difference
    n_new = n 

    # convert back from UTM to geodetic
    (lattitude_new, longitude_new) = uc.utm_to_geodetic(hemisphere, zone, e_new, n_new)

    # calculate the error using Great Circle Distance Formula
    calc_distance=2*asin(sqrt((sin((lattitude-lattitude_new)/2))**2+cos(lattitude)*cos(lattitude_new)*(sin((longitude-longitude_new)/2))**2))
    #calc_distance = d=acos(sin(lat1)*sin(lat3)+cos(lat1)*cos(lat3)*cos(lon1-lon3))
    calc_distance = calc_distance * 6371.0

    error = lattitude_difference - calc_distance
    
    print('Distance: ', lattitude_difference,' Calculated distance: ', calc_distance, 'Error: ',  error)
    return error

def getLongitudeConvertionError(lattitude, longitude, longitude_difference) : 
    (hemisphere, zone, letter, e, n) = uc.geodetic_to_utm (lattitude,longitude)
    e_new = e 
    n_new = n + longitude_difference

    # convert back from UTM to geodetic
    (lattitude_new, longitude_new) = uc.utm_to_geodetic(hemisphere, zone, e_new, n_new)

    # calculate the error using Great Circle Distance Formula
    calc_distance=2*asin(sqrt((sin((lattitude-lattitude_new)/2))**2+cos(lattitude)*cos(lattitude_new)*(sin((longitude-longitude_new)/2))**2))
    # TODO Calc distance is in radians, make sure to multiply with radius of the earth
    calc_distance = calc_distance * 6371.0
    
    #calc_distance = d=acos(sin(lat1)*sin(lat3)+cos(lat1)*cos(lat3)*cos(lon1-lon3))
    error = longitude_difference - calc_distance
    
    print('Distance: ', longitude_difference,' Calculated distance: ', calc_distance, 'Error: ',  error)
    return error


def exercise_4_1():
    # Drone center
    lat1 =  55.47
    lon1 = 10.33
    print("Error @ the Drone Center")
    getLattitudeConvertionError(lat1, lon1,1.)

    # Iceland
    lat1 = 65.887393
    lon1 = 10.33
    print("Error @ Iceland")
    getLattitudeConvertionError(lat1, lon1,1.)

    # Greenland
    lat1 = 81.988262
    lon1 = 10.33
    print("Error @ Greenland")

    getLattitudeConvertionError(lat1, lon1,1.)

    # Longitude test
    lat1 = 55.47
    lon1 = 10.33
    print("Error Longitude Test")
    getLongitudeConvertionError(lat1, lon1,1.)


# instantiate utmconv class
uc = utmconv()

exercise_4_1()
