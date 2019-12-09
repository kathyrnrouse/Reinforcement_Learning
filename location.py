"""
Created on Mon Nov 18 13:45:00 2019
@author Katie Rouse

Apply TrafficFlow to the input json to get the state space
"""

import csv
import pandas as pd
import json
import ast
import datetime
from flow import TrafficFlow
 
class Location:

    def __init__(self, df, integer):
        self.df = df
        self.jsons = []
        self.integer = integer
        self.flow = TrafficFlow()
        self.flow.import_shapes('street shapes')
        self.cam_id = self.df["camera_id"][0]
        self.locs = eval(self.df["locations"][self.integer])
  

    #def get_single_car(self, count):
    #return count

    def get_timestamp(self):
        times = []
        for json_object in self.locs:
            ts = json_object["timestamp"] / 1000
            ts = datetime.datetime.fromtimestamp(ts)
            times.append([ts])
            #print("Object bbox from ({}, {}) to ({}, {}) at {}".format(x1, y1, x2, y2, ts))
            #print(ts)
        return times



    def get_location(self):
        #locs = eval(self.df["locations"][self.integer])
        ret = []
        for json_object in self.locs:
            
            x1, y1, x2, y2 = json_object["coords"]
            ts = json_object["timestamp"] / 1000
            ts = datetime.datetime.fromtimestamp(ts)
            #print("Object bbox from ({}, {}) to ({}, {}) at {}".format(x1, y1, x2, y2, ts))
            #center_x = (x1 + x2) // 2
            #center_y = (y1 + y2) // 2
            #print(center_x,center_y)
            #ret.append((center_x, center_y))
            #print(x1, x2, y1, y2)
            ret.append([x1, y1, x2, y2])
        return ret
    
    def get_box(self):
        foo = self.get_location()
        foo = foo[self.integer]
        #print(foo)
        return foo

    def check_box(self):
        boxes = []
        box = self.get_location()
        for i in range(len(box)):
            goo = box[i]
            
            goo = self.flow.get_position(self.cam_id, goo)
            #print(goo)
            boxes.append([goo])
        return boxes


    def get(self):
        """Returns a JSON object of the currently accrued data"""
        return self.jsons    

    def appender(self):

        new_json = {}
        #new_json["pole_id"] = self.pole_id
        new_json["timestamp"] = self.get_timestamp()
        new_json["locations"] = self.get_location()
        new_json["label"] = self.check_box()
        new_json["camera_id"] = self.cam_id
        #new_json["intersection"] = self.is_intsx
        #new_json["id"] = str(uuid4())

        self.jsons.append(json.dumps(new_json))
        return self.jsons
        
        


