##### TASK #####
'''
In QGIS, given any layer that has any numerical field in its attribute table,
write a Python program to report the number of features that have their value
above the mean of that field. When your data has multiple numerical fields,
you can use any of them to test your code. You should use log message to report.
'''

#####
layer = QgsVectorLayer('C:\\Users\\steve\\OneDrive - The Ohio State University\\5223\\data\\libraries_data_sources\\trt00_shp.shp','tracts','ogr')

features = layer.getFeatures()
areaField = [f['Area'] for f in features] # create new list of the area field
meanArea = sum(areaField)/len(areaField)
aboveMeanCount = 0
for a in areaField:
    if a > meanArea:
        aboveMeanCount += 1
QgsMessageLog.logMessage("{0} tracts with area larger than mean value of {1}".format(str(aboveMeanCount),meanArea), level =Qgis.Info)
