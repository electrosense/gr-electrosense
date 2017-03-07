# this module will be imported in the into your flowgraph
cur=-1.0
fft_arr={}
sim_arr={}
sim_red = 1.05

import numpy as np
import random

def crosscorr(x,y):
    a = np.correlate(x, y, mode='full')
    norm = np.sqrt(np.power(x,2).sum()) *  np.sqrt(np.power(y,2).sum())
    #a = (a - np.mean(a)) / (np.std(a) * len(a))
    #return np.nan_to_num(a)
    return np.nan_to_num(a/norm)

def sim2prob(x):
    return np.exp(x)/np.exp(x).sum()

def upd_sim_arr():
    vals = np.array(sim_arr.values())
    keys = np.array(sim_arr.keys())
    prob = sim2prob(vals)
    prob = prob >= np.random.rand()
    vals[prob]=vals[prob]/sim_red
    for i in range(len(keys)):
        sim_arr[keys[i]] = vals[i]
    return min(sim_arr, key=sim_arr.get)

def step(start,end,incr,val,mode,wt,alpha_s):
    global cur
    global fft_arr, sim_arr

    #sequential scanning
    if mode==0:
        cur=cur+incr
    #random scanning
    elif mode == 1:
        rval = int(((end-start)/incr)+0.5)
        cur=cur+incr*random.randint(1,rval)
    #similarity scanning
    else:
        if(fft_arr.has_key(cur)):
            cc = crosscorr(fft_arr[cur],val)
            delf = cc.max()
            r = np.argmax(cc)
            #print r, wt, delf
            sim  = r * wt + (1-wt) * delf
            if(sim_arr.has_key(cur)):
                pass
            else:
                sim_arr[cur]=0
            sim_arr[cur] = alpha_s * sim + sim_arr[cur] * (1-alpha_s)
            new=upd_sim_arr()
            #print "new:",new
            #print "sim:",sim_arr
        else:
            if(cur>0):
                sim_arr[cur]=0
            new=cur+incr
        fft_arr[cur]= val
        cur=new

    if (cur > end or cur < start):
        cur = start
    #print cur
    return cur

