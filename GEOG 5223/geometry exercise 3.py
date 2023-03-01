## TASK ##

'''Write a Python program to do three things in QGIS:

First, it loads a point feature class from an existing data (a point shapefile, 
for example) into QGIS as a layer. The name of the data file can be fixed. The 
program should check the type of data and make sure it is a point data set. If 
the data is not a point data, the program should repeatedly ask the user to give
the path to a point data. It should not work on the next task unless the point 
data is loaded successfully.

Second, now that the point layer is added, the program will draw a box 
(rectangle) that contains most of the points. By "most," we actually have 
something very specific: we draw a rectangle such that there is at least one 
outside of each of the four sides of the rectangle. The only time multiple 
points can be out of one side of the rectangle is when they all share the same X
or Y coordinate. This rectangle will be added to QGIS as a polygon layer. The 
polygon (rectangle) has an attribute called "Name" and you can assign any value 
to that attribute.

Finally, after the previous two tasks are done, the program will post a log 
message that should contain the name of the two layers added and the number of 
points contained in the rectangle.'''

## INITIALIZATION ##
QgsProject.instance().removeAllMapLayers()  ## clear map
dataFolder = r'C:\\Users\\steve\\OneDrive - The Ohio State University\\5223\\' \
             r'data\\libraries_data_sources\\'

######   MAIN   ######
### first task
cond = True
while cond:
    fileName = (QInputDialog.getText(None, "File name","Enter file name: "))[0]
        # r'public_library_shp.shp' is point feature
        # r'trt00_shp.shp' is polygon feature
    pointLayer = QgsVectorLayer(dataFolder+fileName, 'Points', 'ogr')
    if pointLayer.geometryType() == 0:
        cond = False
    else:
        print('please enter a point shapefile')
QgsProject.instance().addMapLayers([pointLayer])

### second task
#get coordinates of point feature
c = [pointLayer.getFeature(i).geometry() for i in range(0,pointLayer.featureCount())]
coords = [(i.asPoint()[0],i.asPoint()[1]) for i in c] 

#determine rectangle coords
minX = min([p[0] for p in coords])
maxX = max([p[0] for p in coords])
minY = min([p[1] for p in coords])
maxY = max([p[1] for p in coords])
rectangleWKTString = f'POLYGON (({minX+1} {maxY-1}, {minX+1} {minY+1}, {maxX-1} {minY+1}, {maxX-1} {maxY-1}, {minX+1} {maxY-1}))'
rectGeom = QgsGeometry.fromWkt(f'''{rectangleWKTString}''')

#add rectangle as polygon layer
crs_string = pointLayer.crs().authid()
rectLayer = QgsVectorLayer(f'Polygon?crs={crs_string}', "Rectangle", 'memory')
rect = QgsFeature()
rect.setGeometry(rectGeom)
fields = QgsFields()
fields.append(QgsField(name='Name', type=QVariant.String))
rect.setFields(fields)
rect.setAttributes(['rectangle!'])
data_provider = rectLayer.dataProvider()
data_provider.addAttributes(fields)
rectLayer.updateFields()
data_provider.addFeatures([rect])
rectLayer.updateExtents()
QgsProject.instance().addMapLayers([rectLayer])

###Third Task
countPointsWithin = 0
for pointFeature in pointLayer.getFeatures(): # get count of points within rectangle
    pointGeom = pointFeature.geometry()
    if pointGeom.within(rectGeom):
        countPointsWithin +=1
        
QgsMessageLog.logMessage(f'Layers added: {pointLayer.name()}, {rectLayer.name()}. ' +
    f'There are {countPointsWithin} points within the rectangle.' \
    , level =Qgis.Info)






