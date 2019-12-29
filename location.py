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

    def __init__(self, CameraId, CarId):
        self.douglas_json = pd.read_csv(CameraId, usecols = ['camera_id','id','label','timestamp','locations'], index_col='id',engine='python')
        self.df = self.douglas_json[self.douglas_json.label =='car']
        self.jsons = []
        self.car_id = CarId
        self.flow = TrafficFlow()
        self.flow.import_shapes('street shapes')
        self.cam_id = self.df["camera_id"][0]
        self.locations = self.df['locations']
        #self.cam_id = CameraId
  


    def get_car_info(self):
        info = ast.literal_eval(self.locations[self.car_id])
        coo = pd.DataFrame(columns = ['CarId','Time','Coords','Grid-Box'])
        for i in range(len(info)):
            
            ts = info[i]['timestamp']
            coords = info[i]['coords'] # coords is the list of 4 values
            space = self.get_grid(coords)
            entry = [{'CarId':self.car_id, 'Time':ts,'Coords':coords,'Grid-Box':space}]
            coo = coo.append(entry, ignore_index = True)
            
            #print(ider, ts, coords)
        #print(coo)
        return coo
    
    def get_grid(self, locs):
        self.locs = locs
        boxes = []
        grids = self.flow.get_position(self.cam_id, self.locs)
        #print(grids)
        #boxes = boxes.append(grids)
        return grids
            

    def get_date_range(output_df, start_range, end_range): 
       
        start_hour = start_range.hour 
        start_minute = start_range.minute 
        start_second = start_range.second
        start_mili = start_range.microsecond
        cat = str(start_hour) + ':' + str(start_minute)+ ':' + str(start_second) + "."+str(start_mili)
        print("start of range:" ,cat)
        end_hour = end_range.hour
        end_minute = end_range.minute
        end_second = end_range.second 
        end_mili=end_range.microsecond 
        cat2 = str(end_hour)+":"+str(end_minute)+":"+str(end_second) + "." +str(end_mili)
        print("end of range:",cat2)

        print(output_df.between_time(*pd.to_datetime([cat,cat2]).time))


    
