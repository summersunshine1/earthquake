from readdata import *
import numpy as np
import matplotlib.pylab as plt

from getPath import *
from commonLib import *
pardir = getparentdir()

example_dir = pardir + '/example30'

lw = 300
sw = 10

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
    file_list = listfiles(example_dir)
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
            print(sline)
            print(pline)

            lwindows = window(earr, lw)
            swindows = window(earr, sw)
            l = len(lwindows)
            ratio = np.mean(swindows,axis = 1)[:l]/np.mean(lwindows,axis = 1)[:l]
            print(ratio)
            plt.plot(ratio)            
            plt.plot(pindex+1,0,marker='o', color='r')
            plt.plot(sindex+1,0,marker='o', color='r')
            # plt.plot((sindex+1,0), marker='o', color='r')
            
            plt.show()
            dataarr = []
        dataarr.append(data)
        sindex = srelative
        pindex = prelative
        
if __name__=="__main__":
    computstalta()
        
              
                
                
                    
        
        
    
        
 
 
    
    