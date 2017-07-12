from readdata import *
import numpy as np
import matplotlib.pylab as plt
import heapq
from scipy import signal

from getPath import *
from commonLib import *
pardir = getparentdir()

from detectPeaks import *

example_dir = pardir + '/example30'
sample_dir = pardir + '/sample/bfafter'

lw = 1500
sw = 300
# sw = 50
# lw = 3000

def window(fseq, window_size):
    arr = []
    for i in range(len(fseq) - window_size + 1):
        arr.append(fseq[i:i+window_size])
    return arr
        
    # for seq in window('abcdefghij', 3):
        # print seq

def energyfunction(datae,daten,dataz):
    earr = np.square(datae)+np.square(daten)+np.square(dataz)
    return earr
    
def convertline(index):
    a1 = [index+1]
    a2 = [0]
    return list(zip(a2,a1))

def computstalta():
    file_list = listfiles(sample_dir)
    length = len(file_list)
    dataarr = []
    sindex = 0
    pindex = 0
    for i in range(length):
        data, srelative, prelative = getrawData(file_list[i])
        if i%3==0 and not i==0:
            earr = energyfunction(dataarr[0],dataarr[1],dataarr[2])
            # plt.plot(earr)
            sline = convertline(sindex)
            pline = convertline(pindex)
            # print(sline)
            # print(pline)
            # earr =p_eigen_function(earr)
            lwindows = window(earr, lw)
            swindows = window(earr, sw)
            l = len(lwindows)
            ratio = np.mean(swindows,axis = 1)[:l]/np.mean(lwindows,axis = 1)[:l]
            print(ratio)
            plt.plot(ratio)            
            plt.plot(pindex+1,0,marker='o', color='r')
            plt.plot(sindex+1,0,marker='o', color='r')
            plt.plot([0,4000],[0.5,0.5]) 
            # plt.plot((sindex+1,0), marker='o', color='r')
            ratio = list(ratio)
            indexs = heapq.nlargest(2, ratio)
            p = ratio.index(indexs[0])
            s = ratio.index(indexs[1])
            print("real:"+str(pindex)+" "+str(sindex))
            print("predict:"+ str(p+1)+" "+str(s+1))
            plt.show()
            dataarr = []
        dataarr.append(data)
        sindex = srelative
        pindex = prelative
    lens = [len(dataarr[0]),len(dataarr[1]),len(dataarr[2])]
    index = np.argmin(lens)
    l = lens[index]
    earr = energyfunction(dataarr[0][:l],dataarr[1][:l],dataarr[2][:l])
    # plt.plot(earr)
    sline = convertline(sindex)
    pline = convertline(pindex)
    # print(sline)
    # print(pline)
    # earr =p_eigen_function(earr)
    lwindows = window(earr, lw)
    swindows = window(earr, sw)
    l = len(lwindows)
    ratio = np.mean(swindows,axis = 1)[:l]/np.mean(lwindows,axis = 1)[:l]
    print(ratio)
    plt.plot(ratio)            
    # plt.plot(pindex+1,0,marker='o', color='r')
    # plt.plot(sindex+1,0,marker='o', color='r')
    # plt.plot([0,4000],[0.5,0.5]) 
    # plt.plot((sindex+1,0), marker='o', color='r')
    ratio = list(ratio)
    # indexs = heapq.nlargest(2, ratio)
    # p = ratio.index(indexs[0])
    # s = ratio.index(indexs[1])
    # print("real:"+str(pindex)+" "+str(sindex))
    # print("predict:"+ str(p+1)+" "+str(s+1))
    plt.show()
    dataarr = []
        
def p_eigen_function(dataz):
    res = []
    res.append(np.square(dataz[0]))
    for i in range(1,len(dataz)):
        res.append(np.square(dataz[i]-dataz[i-1])+np.square(dataz[i]))
    return res
     
def pwave_find():
    file_list = listfiles(example_dir)
    length = len(file_list)

    for i in range(length):
        if i%3==2:
            data, srelative, prelative = getrawData(file_list[i])
            print(file_list[i])
            res = p_eigen_function(data)
            lwindows = window(res, lw)
            swindows = window(res, sw)
            l = len(lwindows)
            ratio = np.mean(swindows,axis = 1)[:l]/np.mean(lwindows,axis = 1)[:l]
            print(ratio[:10])
            p = detect_peaks(ratio,show=False,mph=0.2, edge='rising')
            plt.plot(ratio)
            plt.plot(prelative+1,0,marker='o', color='r')
            plt.plot(srelative+1,0,marker='o', color='r')
            print(".....")
            print(str(p)+" "+str(np.argmax(ratio)))
            print("real:"+str(prelative)+" "+str(srelative))
            plt.show()
    
        
if __name__=="__main__":
    computstalta()
    # pwave_find()   
              
                
                
                    
        
        
    
        
 
 
    
    