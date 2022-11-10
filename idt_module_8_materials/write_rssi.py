#!/usr/bin/env python3

'''
This script uses bokeh to show radio_status on live updating plots. Makes it easier to experiment with antennas
and see the results in real time.

This script is made by Frederik Mazur Andersen for his Master Thesis
and is taken from his repository: https://gitlab.com/Crowdedlight/dynamic-pathplanner-for-uavs

Revision
2019-03.15 FMA simple version from master thesis included to show rssi in plots
'''

# imports
import rospy
from mavlink_lora.msg import mavlink_lora_radio_status
from datetime import datetime
import signal
from functools import partial

# parameters
mavlink_lora_radio_status_topic = '/mavlink_radio_status'

import csv
import datetime
class rssi_node:
    def __init__(self):

        # launch node
        rospy.init_node('mavlink_lora_radio_status', disable_signals = True)
        ct = datetime.datetime.now()
        self.f = open('rssi-' + str(ct.timestamp()) +'.csv', 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['time', 'rssi', 'remrssi', 'noise', 'remnoise', 'rxerrors', 'fixed'])
        self.time_offset = rospy.get_time()
        self.rate = rospy.Rate(10)

        # install ctrl-c handler
        signal.signal(signal.SIGINT, self.signal_handler)

        # subs
        self.radio_msg_sub = rospy.Subscriber(mavlink_lora_radio_status_topic, mavlink_lora_radio_status,
                                              self.on_mavlink_msg)

        # wait until everything is running
        rospy.sleep(1)

    # define ctrl-c handler
    def signal_handler(self, signal, frame):
        # self.stop_flag = True
        self.radio_msg_sub.unregister()        
        self.f.flush()
        self.f.close()
        print("graceful exit")
        exit()

    def write(self):
        row = [str(self.now),str(self.rssi), str(self.remote_rssi), str(self.noise), str(self.remote_noise), str(self.rx_errors), str(self.fixed)]
        self.writer.writerow(row)

    def on_mavlink_msg(self, msg):
        # save data in file before doing live plot
        self.now = rospy.get_time()
        time = self.now - self.time_offset  # time in sec since start
        self.rssi = msg.rssi
        self.remote_rssi = msg.remrssi
        self.noise = msg.noise
        self.remote_noise = msg.remnoise
        self.rx_errors = msg.rxerrors
        self.fixed = msg.fixed


if __name__ == '__main__':
    rssi = rssi_node()
    while not (rospy.is_shutdown()):
        # do stuff
        rssi.write()

        # sleep the defined interval
        rssi.rate.sleep()
    rssi.f.close()


