##### Task #####
'''
Write a Python program in ArcGIS Pro that does the following tasks:

- Loads a shapefile from your own data as a layer.
- Adds a new TEXT field with a proper name to the attribute table of the layer.
- Update the values in the new field of the layer based on the values of an
existing field in the data.

For the last task, you will need to have a criterion so that the value of the
new field will be "YES" for some values of the existing field and "NO" for other
values of the existing field. Using the public library shapefile as an example
(but you need to use your own data), you could add a filed called In_Columbus
and could use "YES" for those libraries in Columbus and "NO" for the others.
In another example of the tracts, you could set "YES" to the tracts with area
larger than a certain value and "NO" otherwise. Then, our program should also report (print) how many YES values and NO values,
respectively.
'''


## i will use the update cursor to update the new text field if the preexisting
#  area field has a value greater than 1000000 with 'YES' or 'NO'
import arcpy
arcpy.env.workspace = r'C:\\Users\\steve\\OneDrive - The Ohio State University\\5223\\data\\libraries_data_sources'
arcpy.management.CopyFeatures('trt00_shp','duplicate1.shp')
arcpy.management.AddField('duplicate1','AreaOv1mil', 'TEXT')
upcurs = arcpy.UpdateCursor('duplicate1')
for row in upcurs:
    if row.getValue('Area') > 1000000:
        row.setValue('AreaOv1mil','YES')
    else:
        row.setValue('AreaOv1mil','NO')
    upcurs.updateRow(row)
searchCurs = arcpy.SearchCursor('duplicate1.shp', fields='AreaOv1mil')
countYes = 0
countNo = 0
for row in searchCurs:
    if row.AreaOv1mil == 'YES':
        countYes += 1
    else:
        countNo += 1
print("number of tracts with area over 1000000: {0}, number of tracts with area under 1000000: {1}".format(countYes,countNo))
searchCurs.reset()
upcurs.reset()
#output:
#>>number of tracts with area over 1000000: 222, number of tracts with area under 1000000: 42
