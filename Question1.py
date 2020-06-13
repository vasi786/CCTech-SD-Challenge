#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 06:19:14 2020
CCTech June 2020 Software Developer Hiring Challenge
Question 1:
@author: venu Angirekula
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.random  as ran

#%%
#Inputs
Location = {0:'Outside',1:'inside'}
# Polygon Coordinates
Polygon = np.array([[8,3],[3,2],[6,8],[2.5,6],[0.5,4],[5,5]])

def random_coord(mini,maxi):  # get random coordinates between 0-1
    p = mini + ran.random(1)*maxi
    return p
X_max,Y_max = [max(Polygon[:,0]),max(Polygon[:,1])]
X_min,Y_min = [min(Polygon[:,0]),min(Polygon[:,1])]
# Random point 
x,y = [random_coord(X_min,X_max), random_coord(Y_min,Y_max)]
#x,y=[3.9,4]
#%%
def TracingMethod(x,y,Polygon):
    n = len(Polygon)
    loc = 0;

    x1,y1 = Polygon[0]
    for i in range(n+1):
        x2,y2 = Polygon[i%n]       
        
        if y > min(y1,y2) and y <= max(y1,y2):  
            if x <= max(x1,x2):
                if y1 != y2:
                    x_projection = (y-y1)*(x2-x1)/(y2-y1) + x1 
                if (x1==x2 or x <= x_projection): 
                    loc = not loc
#        print('(x1,y1): ',x1,y1,'\t(x2,y2): ',x2,y2,
#              '\t x projection: ', x)
        x1,y1=x2,y2
    return loc



loc = TracingMethod(x, y, Polygon)
print ("\n Location :", Location[loc])

# Visualizing the Polygon and points
plt.plot(np.append(Polygon[:,0],Polygon[0,0]) ,
     np.append(Polygon[:,1],Polygon[0,1]),'-o')
plt.scatter(x,y,color='r')    
#%%