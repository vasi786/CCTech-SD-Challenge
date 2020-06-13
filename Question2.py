#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:23:50 2020
CCTech June 2020 Software Developer Hiring Challenge
Question 2:
@author: venu Angirekula
"""

from Question2_FunctonsFile import *
#%%
# Structures coordinates
B = [[[4,0],[4,-5],[7,-5],[7,0],[4,0]],
               [[0.4,-2],[0.4,-5],[2.5,-5],[2.5,-2],[0.4,-2]]] # last point is added duplicate

# source point
SO = [-3.5,1] 
# Rays info
NOR = 1000 # Number of Rays

#Edges for buildings and ploting them    
Edges = []
for b in B:
    Edges+= [[b[j],b[j+1]] for j in range(0,4)]
    b = np.array(b)
    plt.plot(b[:,0],b[:,1],linewidth=2,linestyle='--')
    
plt.scatter(SO[0],SO[1],color='r',linewidths=5)
#%%
# Remove building basement edges (They are not visible to sunlight )
b = np.array(B[0]);Basement_Level = min(b[:,1])
for i,j in enumerate(Edges):
    if j[0][1]==Basement_Level and j[1][1]==Basement_Level:
        del Edges[i]

rays  = pd.DataFrame(np.zeros([NOR,len(Edges)])) # empty dataframe to store to rays info
rays.loc[:,'x_ori'] = np.zeros(len(rays));rays.loc[:,'y_ori'] = np.zeros(len(rays))
rays.loc[:,'x_inter'] = np.zeros(len(rays));rays.loc[:,'y_inter'] = np.zeros(len(rays))

# Loop for Light rays from the source point 'SO'
for i,j in enumerate(np.arange(-90,5,95/(NOR))):
    IPS = [(1000,1000)] # Initilialize some Intersection point's
    b = rayEnds(SO,j,10)
    Line1 = line(SO,b)
    P1 = Point(SO[0],SO[1]);Q1 = Point(b[0],b[1])  
    for k,l in enumerate(Edges):   #loop over the edges
        P2 = Point(l[0][0],l[0][1]);Q2 = Point(l[1][0],l[1][1])
        Line2 = line(l[0],l[1]) # edge

        if doIntersect(P1,Q1,P2,Q2):
            rays.iloc[i,k] = True
            IPS.append(intersection(Line1,Line2)) # collect Intersection points
        else:
            rays.iloc[i,k] = False
    d = [distance(SO,i) for i in IPS] 
    # Use minimun disance, to acquire first intersection point for a ray
    Intersection_Point = IPS[d.index(min(d))]
    row_sum = sum(rays.iloc[i,:])               
    if row_sum:
        rays.loc[i,'x_ori'] = b[0]
        rays.loc[i,'y_ori'] = b[1]
        rays.loc[i,'x_inter'] = Intersection_Point[0]
        rays.loc[i,'y_inter'] = Intersection_Point[1]
        # Plot only rays that contact the buildings
#        plt.plot([SO[0],b[0]],[SO[1],b[1]],color='g',alpha=0.3)
        plt.plot([SO[0],Intersection_Point[0]],
                 [SO[1],Intersection_Point[1]],
                 color='y',alpha=0.5)
    else:
        rays.drop(rays.index[i]) 

# Drop rays that are not in contact
bool_series = (rays!=0).any(axis=1)
rays = rays.loc[bool_series]

''' Finally, evaluating the exposed length of edges '''
####################################################### 
###############   Exposed Length  #####################
#######################################################
exposedLength = 0 # initialize the exposed length
for i,j in enumerate(Edges):
    x1 = j[0][0]; y1 = j[0][1]
    x2 = j[1][0]; y2 = j[1][1]
    if x1 == x2: # [vertical edge]
        # IMPORTANT: source should be always placed at top side of buildings
        Strikepoints = rays.loc[rays.loc[:,'x_inter']==x1].loc[:,'y_inter']
        if sum(Strikepoints) == 0:
            continue
        ymin = min(Strikepoints)
        ymax = max(Strikepoints)   # y1,y2
        exposedLength += abs(ymax-ymin)
    else: #[Horizontal edge(upper)]
        # IMPORTANT: source should be always placed at left side of buildings
        Strikepoints = rays.loc[rays.loc[:,'y_inter']==y1].loc[:,'x_inter']
        if sum(Strikepoints) == 0:
            continue
        xmax = max(rays.loc[rays.loc[:,'y_inter']==y1].loc[:,'x_inter'])
        xmin = min(Strikepoints)   # x1,x2 
        exposedLength += abs(xmax-xmin)
    
print("Exposed length: \t",exposedLength)

