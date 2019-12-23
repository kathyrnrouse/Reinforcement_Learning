"""
Katie Rouse - 12/12/2019
Experience Replay Buffer
"""

import numbers
import csv
import operator
import random
import csv
import pandas as pd
import json
import ast
import datetime
from flow import TrafficFlow
from datetime import datetime as dt
import numpy as np
import math
from location import Location
from trajectory import speed
from datetime import timedelta, date

def Experience():
    # Make an dataframe that will end up holding the experience buffer:
        # (s): state (8x11)/[(2x1)] matrix (physical spot x [position, speed])
        # (a): dummy value, legal action
        # (r): reward, initialize as 0
        # (s1): new state, same as (s)
        # (d): FALSE
        # (legal_a_one): x in legal action ????
        # (legal_a_one_s1): getLgalAction(ph) ????
    outputData = pd.DataFrame(columns=['CarId','Time','Coords','Grid-Box','Speed'])
    experience_df = pd.DataFrame(columns = ['state','action','reward','s1','d','legal_a_one','legal_a_one_s1'])



    douglas_json = pd.read_csv('mlk-douglas-cam-1.csv', usecols = ['camera_id','id','label','timestamp','locations'],index_col = 'id',engine="python")
    df = douglas_json[douglas_json.label== 'car']
    ids = list(df.index.values)

    #test = len(df)
    test = 2
    for i in range(test):
        """
            buff is the initiation of a Location and iterates through
            the index of the input df, aka unique "id" or car_id's
        """
        buff = Location('mlk-douglas-cam-1.csv',ids[i])
        car = buff.get_car_info()  ## returns an array of [car_id, time, coords, grid-box]
        ## each row of car is an array with time, coords, grid-box being dicts

        for j in range(len(car)):
            entry = car.iloc[j]
            outputData = outputData.append(entry,ignore_index =True)
            ## add on to the empty dataframe 
   
    timestamp = outputData.copy()
    time_df= outputData.copy()
    time_df = time_df['Time']
    loc_df = outputData.copy()
 
    for q in range(len(timestamp)):
        (timestamp['Time'])[q] = datetime.datetime.fromtimestamp((timestamp['Time'])[q]/1000)


    
    max_time = time_df.max()
    end_time= datetime.datetime.fromtimestamp(time_df.max()/1000)
    min_time = time_df.min()
    start_time = datetime.datetime.fromtimestamp(time_df.min()/1000)
    interval = (max_time - min_time)
    pers = math.ceil(interval/1000)

    d_range = pd.date_range(start_time, end_time, periods = pers)
    dates= d_range.to_series()
    

    ranger = len(dates.index)

    timestamp['Datetime'] = pd.to_datetime(timestamp['Time'])
    timestamp = timestamp.set_index('Datetime')
  



    locs = loc_df[['Time','Coords','CarId']].copy()
    locs = locs.set_index('CarId')
    speeds = []
    for dex in locs.index.unique():
        locations = locs.loc[dex]
        vel = speed(locations)
        locations['pixelSpeed'] = vel
        locations['speed mph'] = vel/30
       
        for p in range(len(locations)):
            speeds.append(vel/30)    
    timestamp['Speed'] = speeds  

  
    myBuffer0 = priorized_experience_buffer()
    episodeBuffer0 = priorized_experience_buffer()
   
    for d in range(ranger-2):    
        start_range = dates.index[d]
        end_range = dates.index[d+1]
        foo = get_date_range(timestamp, start_range, end_range)
        state = get_grid_matrix(foo)

        start_next = dates.index[d+1]
        end_next = dates.index[d+2]
        next_state = get_date_range(timestamp,start_next,end_next)
        next_state = get_grid_matrix(next_state)
        action = random.randint(0,9)
        reward = 0
        d = 'FALSE'
        legal_a_one = 0
        legal_a_one_s1 = 0

        #entry = {"state":[state], 'action':[action], 'reward':[reward],'s1:':[next_state], 'd':[d], 'legal_a_one':[legal_a_one], 'legal_a_one_s1':[legal_a_one_s1]}
        #experience_buffer= experience_buffer.append(entry, ignore_index=True)
        episodeBuffer0.add(np.reshape(np.array([state,action,reward,next_state,d,legal_a_one, legal_a_one_s1]),[1,7]))
        #exp_buff.add(experience)
        #print("experience:",episodeBuffer0)
    myBuffer0.add(episodeBuffer0.buffer)

    #print("smaple of 20:")
    #print(myBuffer0.buffer[1])
    return myBuffer0.buffer
   

class priorized_experience_buffer():
    def __init__(self, buffer_size = 20000):
        self.buffer = []
        self.prob = []
        self.err = []
        self.buffer_size = buffer_size
        self.alpha = 0.2
    
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.err[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
            self.prob[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
        self.err.extend([10000]*len(experience))
        self.prob.extend([1]*len(experience))
            
    def updateErr(self, indx, error):
        for i in range(0, len(indx)):
            self.err[indx[i]] = math.sqrt(error[i])
        r_err = ss.rankdata(self.err)  #rank of the error from smallest (1) to largest
        self.prob = [1/(len(r_err)-i+1) for i in r_err]

        
    def priorized_sample(self,size):
        prb = [i**self.alpha for i in self.prob]
        t_s = [prb[0]]
        for i in range(1,len(self.prob)):
            t_s.append(prb[i]+t_s[i-1])
        batch = []
        mx_p = t_s[-1]
        
        smp_set = set()
        
        while len(smp_set)<batch_size:
            tmp = np.random.uniform(0,mx_p)
            for j in range(0, len(t_s)):
                if t_s[j] > tmp:
                    smp_set.add(max(j-1,0))
                    break;
        for i in smp_set:
            batch.append([self.buffer[i], i])
        return np.array(batch)
#         return np.reshape(np.array(random.sample(self.buffer,size)),[size,6])



def get_date_range(output_df,start_range, end_range): 
        out = output_df
        start_hour = start_range.hour 
        start_minute = start_range.minute 
        start_second = start_range.second
        start_mili = start_range.microsecond
        cat = str(start_hour) + ':' + str(start_minute)+ ':' + str(start_second) + "."+str(start_mili)
        #print("start of range:" ,cat)
        end_hour = end_range.hour
        end_minute = end_range.minute
        end_second = end_range.second 
        end_mili=end_range.microsecond 
        cat2 = str(end_hour)+":"+str(end_minute)+":"+str(end_second) + "." +str(end_mili)
        #print("end of range:",cat2)

        partition = out.between_time(*pd.to_datetime([cat,cat2]).time)
        return partition

def get_grid_matrix(output_df):
    p_state = np.zeros((8,13,2))
    valid_spots = [
        (0,2),
        (0,3),
        (1,2),
        (1,3),
        (2,2),
        (2,3),
        (3,0),
        (3,1),
        (3,2),
        (3,3),
        (3,4),
        (3,5),
        (3,6),
        (3,7),
        (3,8),
        (3,9),
        (3,10),
        (4,0),
        (4,1),
        (4,2),
        (4,3),
        (4,4),
        (4,5),
        (4,6),
        (4,7),
        (4,8),
        (5,0),
        (5,1),
        (5,2),
        (5,3),
        (5,4),
        (5,5),
        (5,6),
        (6,2),
        (6,3),
        (7,2),
        (7,3)
    ]

    for p in range(len(output_df)):
        spd = output_df['Speed'][p] 
        box = output_df['Grid-Box'][p]
        if box != None:
            #print("box:",box)
            x = int(box[1])
            #print("x:",x)
            y = int(box[3:-1])
            #print("y:",y)

            p_state[x,y]= [1,int(round(spd))]
    return p_state




