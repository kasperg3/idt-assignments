#!/usr/bin/env python3

import json


class QGCPlanGenerator:
    def __init__(self):

        self.plan = {}
        self.items = []
        self.geoFence = {}
        self.plan['fileType'] = 'Plan'

        self.geoFence['polygon'] = []
        self.geoFence['version'] = 1
        self.plan['geoFence'] = self.geoFence

        self.plan['groundStation'] = 'QGroundControl'

        self.mission = {}
        self.mission['cruiseSpeed'] = 15
        self.mission['firmwareType'] = 3
        self.mission['hoverSpeed'] = 5
        self.mission['vehicleType'] = 2
        self.mission['version'] = 2

        rallyPoints = {}
        rallyPoints['points'] = []
        rallyPoints['version'] = 1
        self.plan['rallyPoints'] = rallyPoints

        self.plan['version'] = 1

    def generate(self):
        self.mission['items'] = self.items
        if "plannedHomePosition" not in self.mission:
            raise RuntimeError("No planned home position set!")

        self.plan['mission'] = self.mission

        plan_json = json.dumps(self.plan, indent=4, sort_keys=True)

        file = open('mission.plan', 'w')
        file.write(plan_json)
        file.close()

    def set_home_position(self, lon, lat, height):
        self.mission['plannedHomePosition'] = [lon, lat, height]

    def add_waypoint(self, lon, lat, height, is_takeoff=False):
        item = {}
        item['autoContinue'] = True
        if is_takeoff:
            item['command'] = 22
        else:
            item['command'] = 16
        item['doJumpId'] = 1
        item['frame'] = 3
        item['params'] = [0, 0, 0, 0, lon, lat, height]
        item['type'] = 'SimpleItem'
        self.items.append(item)
