import arcpy
import os

featureClass = arcpy.GetParameterAsText(0)
featureClassUniqueField = arcpy.GetParameterAsText(1)
outputFolder = arcpy.GetParameterAsText(2)

d = {row[0]:row[1] for row in arcpy.da.SearchCursor(featureClass, ['OID@', featureClassUniqueField])}
print (d)
keys = list(d.keys())
values = list(d.values())

# get related table based on featureClass name
# add '__ATTACH' to featureClass name
attachmentsTable = featureClass + '__ATTACH'

with arcpy.da.SearchCursor(attachmentsTable, ['DATA', 'ATT_NAME', 'REL_OBJECTID', 'ATTACHMENTID']) as cursor:
    for row in cursor:
        if row[2] in d:
            arcpy.AddMessage(str(row[2]) + " " + str(values[keys.index(row[2])]) + " " + str(row[1]))
            attachment = row[0]
            filename = str(values[keys.index(row[2])]) + '_' + str(row[1])
            open(outputFolder + os.sep + filename, 'wb').write(attachment.tobytes())
            del row
            del filename
            del attachment
            
del cursor