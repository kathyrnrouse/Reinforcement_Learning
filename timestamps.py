import datetime
import pandas as pd

from flow import TrafficFlow
from location import Location

def main():
    df = []
    outputData = pd.DataFrame(columns=['Time','Location','Box', 'CarID'])
    douglas = pd.read_csv("mlk-douglas-cam-1.csv")
    #douglas = douglas[douglas.label== 'car']
    # Normally, iterate through every row in the "locations" col
    # eval should do the job, and takes care of the inner dicts too
    test = 1


    for i in range(test):
        
        
        loc = eval(douglas["locations"][i])
        id_one = douglas["id"][0]
        # here you can see the list, that it is type list, and that its contents are dicts
        #print(locs, type(locs), type(locs[0]))
    
        buff = Location(douglas, 1)
        #box = buff.check_box()
        #print(box)
        buff.get_location()
        
        buff.check_box()
        buff.get_timestamp()
        

        #entry=[{'Time':buff.get_timestamp(), 'buff.get_location(),buff.check_box(),douglas["id"][i]}]
        #print(entry)
        print(buff.appender())
        #df = df.append(entry, ignore_index = True)
        outputData = outputData.append(entry, ignore_index = True)
    print(outputData)
   
    
    
    df = outputData.copy()
    #print(df['Time'][])
    print(df.index)
    times = []
    """
    for interval in df['Time']:
        for j in range(len(interval)):
            json = interval[j]
            
            #ts = json/ 1000
            #ts = datetime.datetime.fromtimestamp(ts)
            #times.append([ts])
            print(json)
    print(times)
    """
    #new = df.groupby(pd.Grouper(level= 'Time', freq='5s', axis = 1))
    #as_index=False).apply(lambda x: x['Box'])
    #df['period'] = new.index.get_level_values(0)
    #print(df) 
   
    ## convert the index to integer value so we can sum up to the hour
 
    #groups = df.groupby(df.index//)
    
    

if __name__ == "__main__":
    main()



