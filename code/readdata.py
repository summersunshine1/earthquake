from obspy import read
from datetime import datetime,timedelta
import pandas as pd
import matplotlib.pylab as plt
import os
import numpy as np

from statsmodels.tsa.seasonal import seasonal_decompose
from getPath import *
from commonLib import *
pardir = getparentdir()

example_dir = pardir + '/example30'
sample_dir = pardir + '/sample/bfafter'

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
    
def line(times, index):
    ptime = [times[index] for i in range(10)]
    p_data = [t for t in range(-5000,5000, 1000)]
    p_data = convert_array_to_frame(p_data, ptime)
    return p_data

def getData(path):
    st = read(path)
    stat = st[0].stats
    # print(stat)
    delta = stat.delta
    begin_time = stat.starttime
    end_time = stat.endtime
    times = generatetime(begin_time, end_time, delta)
    begin_date_time = get_datetime_from_time(begin_time)
   
    data = st[0].data
    
    btime = stat.sac.b
    etime = stat.sac.e
    s_line = line(times, 0)
    p_line = line(times,0)
    if 't0' in stat.sac:
        stime = stat.sac.t0
        srelative = stime-btime
        srelative = int(srelative/delta)
        s_line = line(times, srelative)
    if 'a' in stat.sac:
        ptime = stat.sac.a
        prelative = ptime-btime
        prelative = int(prelative/delta)
        p_line = line(times, prelative) 
    frame = convert_array_to_frame(data, times)
    print(srelative-prelative)
    return p_line, s_line, frame
    
def decompose(ts):  
    decomposition = seasonal_decompose(ts[2], freq=72)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    p = plt.subplot(311)
    p.plot(trend)
    p.plot(ts[0],color = 'g')
    p.plot(ts[1],color = 'r')   
    p = plt.subplot(312)
    p.plot(seasonal)
    p.plot(ts[0],color = 'g')
    p.plot(ts[1],color = 'r')  
    p = plt.subplot(313)
    p.plot(residual)
    p.plot(ts[0],color = 'g')
    p.plot(ts[1],color = 'r')
    plt.show()

def readfile():
    file_list = listfiles(example_dir)
    i = 0
    length = len(file_list)
    dataarr = []
    filearr = []
    for i in range(length):
        print(file_list[i])
        p_line, s_line, frame = getData(file_list[i])
        if i%3==0 and not i == 0:
            # for j in range(3):
                # decompose(dataarr[j])
            for j in range(3):
                p = plt.subplot(310+j+1)
                p.plot(dataarr[j][2]-np.mean(dataarr[j][2]))
                print(np.mean(dataarr[j][2]-np.mean(dataarr[j][2])))
                p.plot(dataarr[j][0],color = 'g')
                p.plot(dataarr[j][1],color = 'r')    
                
                # p.plot(pd.rolling_mean(dataarr[j][2], window=2))
                # p.plot(pd.rolling_std(dataarr[j][2], window=2))
                plt.title(filearr[j])
            plt.show()
            dataarr = []
            filearr = []
        dataarr.append([p_line, s_line, frame])
        filearr.append(os.path.basename(file_list[i]))
    for j in range(3):
        p = plt.subplot(310+j+1)
        p.plot(dataarr[j][2])
        p.plot(dataarr[j][0],color = 'g')
        p.plot(dataarr[j][1],color = 'r')             
        plt.title(filearr[j])
    plt.show()
    
if __name__=="__main__":
    readfile()
    