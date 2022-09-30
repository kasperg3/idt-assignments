#!/usr/bin/env python3
from cProfile import label
from cmath import log10
import math
from turtle import title
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def getFresnel(d1, d2, frequency, fresnelZone=1):
    """_summary_

    Args:
        d1 (_type_): Distance from Tx to obstacle in km
        d2 (_type_): Distance from obstacle to Rx in km
        frequency (_type_): Frequency in GHz

    Returns:
        _type_: _description_
    """

    # C = 299792458
    # wavelength = C/(frequency*1000000000)
    # return (math.sqrt((fresnelZone*frequency*1000000000*(d1*d2*1000))/((d1+d2)*1000)))

    return (17.3 * (math.sqrt((d1*d2)/(frequency * (d1+d2)))))


def plotFresnelZones(d1, d2, xlim=[-1, 201], ylim=[-50.0, 50.0], showPlot=True, title='Fresnel zones'):
    plt.figure()
    plt.title(title)
    ax = plt.gca()
    center = ((d1+d2)/2)*1000
    zoneWidth = (d2+d1)*1000
    print("0.433GHz", getFresnel(d1, d2, 0.433), "m")
    print("2.400GHz: ", getFresnel(d1, d2, 2.4), "m")
    print("5.800GHz", getFresnel(d1, d2, 5.8), "m")
    ellipse433 = Ellipse(xy=(center, 0.0), width=zoneWidth, height=2*getFresnel(
        d1, d2, 0.433), edgecolor='r', fc='None', lw=2, label="0.433MHz")
    ellipse2400 = Ellipse(xy=(center, 0.0), width=zoneWidth, height=2*getFresnel(
        d1, d2, 2.4), edgecolor='g', fc='None', lw=2, label="2.4MHz")
    ellipse5800 = Ellipse(xy=(center, 0.0), width=zoneWidth, height=2*getFresnel(
        d1, d2, 5.8), edgecolor='b', fc='None', lw=2, label="5.8MHz")
    ax.add_patch(ellipse433)
    ax.add_patch(ellipse2400)
    ax.add_patch(ellipse5800)
    plt.legend()
    ax.set_ylabel("Height [m]")
    ax.set_xlabel("Length [m]")
    plt.xlim([-1, zoneWidth+1])
    plt.ylim(ylim)
    plt.savefig('fresnel' + str(d1) + str(d2) + '.png')
    if showPlot:
        plt.show()


def radioLinkBudget(distance, txFrequency, txPower, txLineLoss, txAntennaGain, rxLineLoss, rxAntennaGain, rxSensitivity):
    """_summary_

    Args:
        distance (_type_): in meters
        txFrequency (_type_): transmitter frequency in MHz
        txPower (_type_): transmitter power in mW
        rxSensitivity (_type_): rx sensitivity in db 
    """
    # Tx gain is the transmitted output power + the tx line loss + antenna gain
    txPower = 10.*math.log10(txPower)
    txGain = txPower + txLineLoss + txAntennaGain
    print("Tranmission gain: ", txGain)

    # Link loss (free space path loss + polarization, aperture, fresnell zone, doppler effect and fading)
    freeSpacePathLoss = -20*math.log10((4*math.pi*txFrequency*distance)/300)
    linkLoss = freeSpacePathLoss
    print("Link loss:", linkLoss)

    # Reciever sensitivity (recieving antenna gain + transmission line loss, + required minimum signal power, all expressed in dB)
    # Margin, a good rule of thumb is that the margin should at least be 30dB
    rxGain = rxLineLoss + rxAntennaGain
    margin = txGain + linkLoss + rxGain - rxSensitivity
    print("Margin:", margin)


# 2.4GHz C2 link: https://ardupilot.org/copter/docs/common-sik-telemetry-radio.html
# https://www.silabs.com/wireless/proprietary/si10xx-sub-ghz-mcps
# Receiver sensitivity to -121 dBm
# Transmition power up to 100mW
# air data rates up to 250kbps
# 2dBi antenna rx/tx
# 15 m of transmission line to the antenna LMR-400 coaxial cable, which will give you about 2 dB loss at 433 MHz for each run.


# 433MHz telemetry link
print("###########link budget 433Mhz###########")
radioLinkBudget(2000, 433, 100, -1, 2, -1, 2, -121)

print("###########link budget 2400Mhz###########")
radioLinkBudget(2000, 2400, 100, -1, 2, -1, 2, -121)

# 5.8GHz video downlink
print("###########link budget 5800Mhz###########")
radioLinkBudget(2000, 5800, 100, -1, 2, -1, 2, -121)

# Example of fresnel zones
print("simple example:")
plotFresnelZones(3, 7, title="Simple Example")

# example: Drone 50m above ground, operator 0.5m, distance between 400m
print("Clearence @ 400m:")
C = math.sqrt(0.0005**2 + 0.400**2)
D = math.sqrt(0.0495**2 + C**2)
plotFresnelZones(D/2., D/2., ylim=[-10, 10], title="400 meter")


# Example: Same as above but at 200m and a building at 100m
print("Clearence @ 200m:")
C = math.sqrt(0.0005**2 + 0.200**2)
D = math.sqrt(0.0495**2 + C**2)
plotFresnelZones(D/2., D/2., ylim=[-10, 10], title="200 meter")
