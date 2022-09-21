#!/usr/bin/env python3
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def getFresnel(d1, d2, frequency):
    """_summary_

    Args:
        d1 (_type_): Distance from Tx to obstacle in km
        d2 (_type_): Distance from obstacle to Rx in km
        frequency (_type_): Frequency in GHz

    Returns:
        _type_: _description_
    """
    return (17.3 * (math.sqrt((d1*d2)/(frequency * (d1+d2)))))/1000


def plotFresnelZones(d1, d2, xlim=[-1, 11], ylim=[-0.05, 0.05], showPlot=False):
    plt.figure()
    plt.title('Fresnel zones')
    ax = plt.gca()
    print("0.915GHz", getFresnel(d1, d2, 0.915)*1000, "m")
    print("2.400GHz: ", getFresnel(d1, d2, 2.4)*1000, "m")
    print("5.800GHz", getFresnel(d1, d2, 5.8)*1000, "m")
    ellipse433 = Ellipse(xy=(5.0, 0.0), width=10, height=2*getFresnel(
        d1, d2, 0.915), edgecolor='r', fc='None', lw=2)
    ellipse2400 = Ellipse(xy=(5.0, 0.0), width=10, height=2*getFresnel(
        d1, d2, 2.4), edgecolor='g', fc='None', lw=2)
    ellipse5800 = Ellipse(xy=(5.0, 0.0), width=10, height=2*getFresnel(
        d1, d2, 5.8), edgecolor='b', fc='None', lw=2)
    ax.add_patch(ellipse433)
    ax.add_patch(ellipse2400)
    ax.add_patch(ellipse5800)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig('fresnel.png')
    if showPlot:
        plt.show()


def radioLinkBudget(distance, txFrequency, txPower, txLineLoss, txAntennaGain, rxLineLoss, rxAntennaGain, rxSensitivity):
    """_summary_

    Args:
        distance (_type_): in km
        txFrequency (_type_): transmitter frequency in MHz
        txPower (_type_): transmitter power in mW
        rxSensitivity (_type_): rx sensitivity in db 
    """
    # Tx gain is the transmitted output power + the tx line loss + antenna gain
    txPower = 10.*math.log10(txPower)
    txGain = txPower + txLineLoss + txAntennaGain
    print("Tranmission gain: ", txGain)

    # Link loss (free space path loss + polarization, aperture, fresnell zone, doppler effect and fading)
    freeSpacePathLoss = - \
        (32.4 + 20*math.log10(txFrequency) + 20*math.log10(distance))
    linkLoss = freeSpacePathLoss
    print("Link loss:", linkLoss)

    # Reciever sensitivity (recieving antenna gain + transmission line loss, + required minimum signal power, all expressed in dB)
    # Margin, a good rule of thumb is that the margin should at least be 30dB
    rxGain = rxSensitivity + rxLineLoss + rxAntennaGain
    margin = txGain + linkLoss - rxGain
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
radioLinkBudget(2, 433, 100, -1.5, 2, -1.5, 2, -126)

print("###########link budget 2400Mhz###########")
radioLinkBudget(2, 2400, 100, -1.5, 2, -1.5, 2, -126)

# 5.8GHz video downlink
print("###########link budget 5800Mhz###########")
radioLinkBudget(2, 5800, 100, -1.5, 2, -1.5, 2, -126)

# Example of fresnel zones
print("simple example:")
plotFresnelZones(3, 7)

# example: Drone 50m above ground, operator 0.5m, distance between 400m
print("Clearence @ 400m:")
C = math.sqrt(0.0005**2 + 0.400**2)
D = math.sqrt(0.0495**2 + C**2)
plotFresnelZones(D/2., D/2., ylim=[-0.01, 0.01])


# Example: Same as above but at 200m and a building at 100m
print("Clearence @ 200m:")
C = math.sqrt(0.0005**2 + 0.200**2)
D = math.sqrt(0.0495**2 + C**2)
plotFresnelZones(D/2., D/2., ylim=[-0.01, 0.01])
