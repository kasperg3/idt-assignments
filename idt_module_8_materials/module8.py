#!/usr/bin/env python3
C = 299792458 # Speed of light m/s
Cc = C * (2/3)
frequency = 1000000 * 434
wavelength = Cc / frequency
antenna_legth = 0.5*wavelength

print("Antenna length", wavelength)
print("Antenna length", antenna_legth)
print("dipole length", antenna_legth/2)



# results
# 18 cm Too long

# 