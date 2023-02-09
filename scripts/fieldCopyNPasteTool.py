'''
USE OF THIS SCRIPT: This script is particular useful for when you have a pair of same row size feature classes, tables, or combination and you want to copy the values
of a field from the source table/feature into a field in the destination table/feature. With modification of the code in under the main section and respective parameters
in ArcGIS, you can reshape this script for the amount of fields you wish to copy at a certain time.

NOTE: the code as it is right now requires 4 mandatory parameters to be configured in ArcGIS: source layer, destination layer, source field1, destination field1. You must
configure the parameters with correct data types. Also, the code now includes 6 additional pairs of source/destination fields so those must be entered in the parameter
tab under script tool properties if you wish to run the code as is.
'''
import arcpy
### function initialization ###
def fieldCopyNPaste(sourceLayer, destLayer, sourceField, destField):
    sourceCursor = arcpy.da.SearchCursor(sourceLayer, sourceField)
    indValue = 0
    for row in sourceCursor:
        with arcpy.da.UpdateCursor(destLayer, destField, "index={0}".format(indValue)) as cursor:
            for row1 in cursor:
                cursor.updateRow(row)
                continue
        indValue = indValue + 1
    return

def indexCreator(destLayer):
    #this function creates an index field in the destination layer in order for fieldCopyNPaste() to properly iterate.
    indexValue = 0
    arcpy.management.AddField(destLayer, "index", "SHORT")
    with arcpy.da.UpdateCursor(destLayer, "index") as cursor:
        for row in cursor:
            row[0] = indexValue
            indexValue = indexValue + 1
            cursor.updateRow(row)
            continue
        
# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    ### Collect parameters and prepare for function calls
    sourceLayer = arcpy.GetParameterAsText(0)
    destLayer = arcpy.GetParameterAsText(1)
    
    sourceField = arcpy.GetParameterAsText(2)
    destField = arcpy.GetParameterAsText(3)
    
    sourceField2 = arcpy.GetParameterAsText(4)
    destField2 = arcpy.GetParameterAsText(5)
    
    sourceField3 = arcpy.GetParameterAsText(6)
    destField3 = arcpy.GetParameterAsText(7)
    
    sourceField4 = arcpy.GetParameterAsText(8)
    destField4 = arcpy.GetParameterAsText(9)
    
    sourceField5 = arcpy.GetParameterAsText(10)
    destField5 = arcpy.GetParameterAsText(11)
    
    sourceField6 = arcpy.GetParameterAsText(12)
    destField6 =  arcpy.GetParameterAsText(13)
    
    sourceField7 = arcpy.GetParameterAsText(14)
    destField7 = arcpy.GetParameterAsText(15)
    
    fieldDict  = {
        sourceField2 : destField2,
        sourceField3 : destField3,
        sourceField4 : destField4,
        sourceField5 : destField5,
        sourceField6 : destField6,
        sourceField7 : destField7,
    }
    ### function calls
    indexCreator(destLayer)
    fieldCopyNPaste(sourceLayer, destLayer, sourceField, destField)
    for key in fieldDict:
        if key != '' or fieldDict[key] != '':
            fieldCopyNPaste(sourceLayer, destLayer, key, fieldDict[key])
    arcpy.management.DeleteField(destLayer, "index")
    
