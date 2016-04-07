# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 09:10:31 2016

@author: poa11
"""
import numpy as np
import matplotlib.pyplot as plt
import time

fp = open('_20160406142458_VIC.txt','r');
newdata = fp.readlines()

newdata = newdata[0:6100]

V = np.zeros(len(newdata))
I = np.zeros(len(newdata))
x = np.arange(0, len(newdata), 1)
i=0

j=0
P = 0

for data in newdata:
    V[i] = data.split(' ')[0]
    I[i] = data.split(' ')[1]
    if (I[i]) > 0:
        j+=1;
        #P+=(I[i])
        P+=(I[i]*V[i])        
        
    i=i+1

print 'avg(V*I) = ' , (P/j)/3600 
print 'S = ' , j 

fig, ax1 = plt.subplots()

ax1.plot(x, V, 'b-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Voltage(V)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
    
ax2 = ax1.twinx()
ax2.plot(x, I, 'r-')
ax2.set_ylabel('Electric current(A)', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
    
plt.show()
