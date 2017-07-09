from obspy import read
from datetime import datetime,timedelta
import pandas as pd
import matplotlib.pylab as plt

from getPath import *
from commonLib import *
pardir = getparentdir()

example_dir = pardir + '/example30'

def generatetime(begin_time, end_time, delta):
    begin_time = datetime.strptime(str(begin_time), "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(str(end_time), "%Y-%m-%dT%H:%M:%S.%fZ")
    t = begin_time
    times = []
    while t<=end_time:
        times.append(t)
        t = t + timedelta(seconds = delta)
    return times
    
def convert_array_to_frame(data, time):
    data = pd.DataFrame(data)
    newtime = pd.DatetimeIndex(time)
    data.index = newtime
    return data
    
def get_datetime_from_time(begin_time):
    begin_time = datetime.strptime(str(begin_time), "%Y-%m-%dT%H:%M:%S.%fZ")
    return begin_time

def getData(path):
    st = read(path)
    stat = st[0].stats
    delta = stat.delta
    print(delta)
    begin_time = stat.starttime
    end_time = stat.endtime
    times = generatetime(begin_time, end_time, delta)
    begin_date_time = get_datetime_from_time(begin_time)
   
    data = st[0].data
    btime = stat.sac.b
    etime = stat.sac.e
    ptime = stat.sac.a
    prelative = ptime-btime
    prelative = int(prelative/delta)
    
    ptime = [times[prelative] for i in range(5) ]
    p_data = [t for t in range(-2000,3000, 1000)]
    p_data = convert_array_to_frame(p_data, ptime)
    
    frame = convert_array_to_frame(data, times)
    plt.plot(frame)
    plt.plot(p_data)
    # plt.scatter(p_data,ptime)
    plt.show()
    

def readfile():
    filelist = listfiles(example_dir)
    for file in filelist:
        getData(file)
        break
    
if __name__=="__main__":
    readfile()
    