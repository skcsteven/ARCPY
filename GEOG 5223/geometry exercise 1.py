###### TASK ######

'''Write a Python program using arcpy to find the south-most point for any given feature class.
Test your code on at least two different types of features (points, lines, or polygons).
The program must be run outside ArcGIS Pro. Submit the code in a .py file
and screenshots showing your test results.'''

## INITIALIZATION ##
'''this file must be run through the arcgis IDLE environment,
i.e "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Scripts\idle.exe"'''

import arcpy
folder = r'C:\\Users\\steve\\OneDrive - The Ohio State University\\5223\\data\\libraries_data_sources\\'
file1 = r'\\trt00_shp.shp' #polygons
file2 = r'\\public_library_shp.shp' #points

def findSouthest(shpFilePath):
    '''this function will print the southern most point's coordinates from an inputted shapefile'''
    sCurs = arcpy.da.SearchCursor(shpFilePath,['SHAPE@'])
    southest = [0,99999999999]
    for row in sCurs:
        poly = row[0]
        if poly.type == 'point':
            if poly.firstPoint.Y < southest[1]:
                southest = [poly.firstPoint.X,poly.firstPoint.Y]
            pass
        else: # check all the points in each polygon
            for each in poly: 
                for point in each:
                    if point.Y < southest[1]:
                        southest = [point.X,point.Y]
    print(f'The southern most point in feature class: {shpFilePath} is {southest}')
    sCurs.reset()

   

## MAIN ##
findSouthest(folder+file1)
findSouthest(folder+file2)
