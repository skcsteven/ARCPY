'''
GEOG 5222 Final Project - Drawing Choropleth Maps from Shapefile with Python
Author: Steve Chen

Objective: Project 2
Write a Python program to draw choropleth maps given a polygon shapefile, a quantitative attribute to map,
the number of classes, and a classification method. The program must implement at least two classification methods.
Please follow the color suggestions at colorbrewer.org Links to an external site. to choose the colors.
Your code should not be fixed to one shapefile. Instead, it should be flexible for any polygon shapefile.

USER NOTES: In order to run, you must modify lines marked by "###EDIT###" to match the folder that your shapefile of interest is within.
Also, the shapex module within the geom git repository @ https://github.com/gisalgs/geom authored by Professor Ningchuan Xiao
is required to be within the same path as the shapefile.

Credits: Professor Ningchuan Xiao at The Ohio State University, Teaching Assistant Ruixuan Ding 
'''

##################################################
### -------------Imports/Functions------------ ###
##################################################


import sys
pth = "C:\\Users\\steve\\OneDrive - The Ohio State University\\5222\\gisalgs\\" ###EDIT###
sys.path.append(pth)
from geom1.shapex import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Patch

def make_path(polygon):
    '''Creates a matplotlib path for a polygon that may have holes.
    
    This function requires to import the following modules
       from matplotlib.path import Path
       from matplotlib.patches import PathPatch

    Input: 
       polygon     [ [ [x,y], [x,y],... ],    # exterior
                     [ [x,y], [x,y],... ],    # first interior ring (optional)
                     [ [x,y], [x,y],... ],   # second interior ring (optional)
                     ... ]                   # there can be more rings (optional)
    Output:
       path: a Path object'''
    
    def _path_codes(n):
        codes = [Path.LINETO for i in range(n)]
        codes[0] = Path.MOVETO
        return codes

    verts = []
    codes = []
    for ring in polygon:
        verts.extend(ring)
        codes += _path_codes(len(ring))
    return Path(verts, codes)

##############################################################
###-------------------- USER INPUTS -----------------------###
##############################################################

### get and check validity of shapefile name from user
cond = True
while cond:
    try:
        fname = input("Enter the name of the shapefile (with .shp): ")
        shp = shapex(pth+'data\\'+fname) ###EDIT###
        hasPoly = False
        for each in shp:
            if each['geometry']['type'] == 'Polygon' or each['geometry']['type'] == 'MultiPolygon':
                hasPoly = True
                break
        if hasPoly == False:
            print('Make sure there are polygons or multipolygons in shape file')
            continue
        if type(len(shp)) == int:
            cond = False
            print("File is valid")
    except:
        print('ERROR --- file name was not valid')

### print basic information of shapefile
print("Number of features: {}".format(len(shp)))
f = shp[0]
print("Number of attributes: {}".format(len(f['properties'])))
at = [each for each in f['properties'].keys()]
print("Attributes: {}".format(at))

### get and check validity of attribute to classify
cond = True
while cond:
    aName = input("Enter the attribute you wish to classify (as seen above without quotes): ")
    if aName in at:
        vals = [i['properties'][aName] for i in shp]
        if all(isinstance(i, int) for i in vals) or all(isinstance(i, float) for i in vals): #ensure numeric attribute type
            cond = False
        else:
            print('ERROR --- Attribute name valid but type is non-numeric')
    else:
        print('ERROR --- attribute name was not valid, please try again')

### get class count, classification type
cond = True
while cond:
    try:
        numClass = int(input("Enter the amount of classes you wish to use: (min 3, max 7) ")) #limit is in place due to color limit below
        if numClass < 3 or numClass > 7:
            print('make sure integer is above or equal to 3 and less than or equal to 7')
        else:
            print('Success, class count == ', numClass)
            cond = False
    except:
        print('ERROR --- value entered was not an integer')
cond = True
c = { 1 : 'Equal Interval Classification', 2 : 'Quantile Classification'}
while cond:
    try:
        cType = int(input("Enter the classification type: (1 for Equal Interval, 2 for Quantile)"))
        if cType != 1 and cType != 2:
            print('Make sure you enter either 1 or 2')
        else:
            print('Success, classification method == ', c[cType])
            cond = False
    except:
        print('ERROR --- value entered was invalid')

###########################################################################
### ---------- plot shapefile with and without classification --------- ###
###########################################################################

### plot shapefile without classification###
        
fig = plt.figure(figsize=(12,3.5))

ax = fig.add_subplot(121) # print the shapefile without classification as reference
for i in range(len(shp)):  # add patches for each polygon/multipolygon in shapefile
    try: # add patch for each polygon
        feature = shp[i]
        fCrd = feature['geometry']['coordinates'] # get coordinates for each polygon w or without holes
        path1 = make_path(fCrd)
        ax.add_patch(PathPatch(path1, facecolor='#d0dbd8', edgecolor='white'))
    except: # polygons that fail the above code are multipolygons
        if len(fCrd) > 1:  # multipolygon testing
            parts = len(fCrd)
            cnt = 0
            while cnt < parts: # print each polygon within the multipolygon
                path1 = make_path(fCrd[cnt])
                ax.add_patch(PathPatch(path1, facecolor='#d0dbd8', edgecolor='white'))
                cnt += 1

### plot shapefile with classification of choice###
                
ax2 = fig.add_subplot(122) # classified shapefile subplot
## preset colors from color brewer in hex format
colors={
    3 : ['#fee0d2','#fc9272','#de2d26'],
    4 : ['#fee5d9','#fcae91','#fb6a4a','#cb181d'],
    5 : ['#fee5d9','#fcae91','#fb6a4a','#de2d26','#a50f15'],
    6 : ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#de2d26','#a50f15'],
    7 : ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d'],
    }

if cType == 1: # equal interval classification type
    mn = min(vals)
    mx = max(vals)
    intervalWidth = (mx-mn) / numClass # get width for each interval
    intervals = [(x * intervalWidth) + mn for x in range(numClass+1)]  # create list with equal interval bounds
    for j in range(0,numClass): # iterate through each interval bound
        intColor = colors[numClass][j] # get face color for each interval from the above color dictionary
        for i in range(len(shp)):  # iterate through each feature in shapefile to see if in interval
            if shp[i]['properties'][aName] >= intervals[j] and shp[i]['properties'][aName] <= intervals[j+1]: # plot if true
                try: # add patch for each polygon
                    feature = shp[i]
                    fCrd = feature['geometry']['coordinates'] # get coordinates for each polygon w or without holes
                    path1 = make_path(fCrd)
                    ax2.add_patch(PathPatch(path1, facecolor=intColor, edgecolor='white'))
                except: # polygons that fail the above code are multipolygons
                    if len(fCrd) > 1:  # multipolygon testing
                        parts = len(fCrd)
                        cnt = 0
                        while cnt < parts: # plot each polygon within the multipolygon
                            path1 = make_path(fCrd[cnt])
                            ax2.add_patch(PathPatch(path1, facecolor=intColor, edgecolor='white'))
                            cnt += 1

else: # quantile classification type
    cPerQuant = len(shp) // numClass # cPerQuant is the amount of features to be added in each class
    if cPerQuant != len(shp) / numClass: # this condition is true when feature count isnt divisible by class number, resulting in slightly non even intervals
        print('Beware: Class number selected resulted in slightly uneven quantiles')
    ### order the coords by numeric attribute value -- shp[i]['properties'][aName]
    ls = [shp[l] for l in range(len(shp))] # make a list copy of shape class in order to sort
    ls.sort(key= lambda x: x['properties'][aName]) # sort by attribute value from least to greatest
    fCnt = 0 # counter until cPerQuant is reached, when reached it will reset and cause color to change
    color = 0 # determines color
    intervals = [ls[0]['properties'][aName]] # keep track of interval bounds for legend
    for i in range(len(ls)):  # plot through each feature, changing color when cPerQuant is reached and then reset to 0 and repeat
        try: # add patch for each polygon
            feature = ls[i]
            fCrd = feature['geometry']['coordinates'] # get coordinates for each polygon w or without holes
            path1 = make_path(fCrd)
            ax2.add_patch(PathPatch(path1, facecolor=colors[numClass][color], edgecolor='white'))
        except: # polygons that fail the above code are multipolygons
            if len(fCrd) > 1:  # multipolygon testing, how many polygons contained
                parts = len(fCrd)
                cnt = 0
                while cnt < parts: # print each polygon within the multipolygon
                    path1 = make_path(fCrd[cnt])
                    ax2.add_patch(PathPatch(path1, facecolor=colors[numClass][color], edgecolor='white'))
                    cnt += 1
        fCnt += 1 # increases per feature added
        if fCnt == cPerQuant: # once the interval reaches the count determined in accordance to quantile classification
            fCnt = 0 # reset the counter for each interval to 0 to begin next interval
            if color != numClass - 1: # need this condition when quantiles exceed cPerQuant due to uneven division
                color += 1 # change the color
            intervals.append(ls[i]['properties'][aName])
    attLs = [x['properties'][aName] for x in ls]
    intervals[len(intervals)-1] = max(attLs) #this and the line above ensure correct legend in case of uneven quantiles

fig.suptitle(fname.upper(),fontsize='xx-large')
ax.set_aspect(1)
ax.grid()
ax.axis('scaled')
ax.set_title('Non-Classified ',fontsize = 'medium')

ax2.set_aspect(1)
ax2.grid()
ax2.axis('scaled')
ax2.set_title(c[cType]+' by '+aName,fontsize = 'medium')
legendElements = [Patch(facecolor=colors[numClass][i],label=str(round(intervals[i],2))+'-'+str(round(intervals[i+1],2))) for i in range(len(colors[numClass]))]
ax2.legend(handles=legendElements,loc='best',fontsize='small')

plt.show()
        
