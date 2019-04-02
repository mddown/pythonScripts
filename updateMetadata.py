# batch update metadata for datasets in a folder
import os, sys
import arcpy
import xml.etree.ElementTree as ET

# arcpy environments
arcpy.env.overwriteOutput = "True"

# Script arguments...
workspace = r'path\to\workspace\geodatabase'
arcpy.env.workspace = workspace
walk = arcpy.da.Walk(workspace, datatype="FeatureClass")
feature_classes = []
sourceMeatadata = r'path\to\MetaDataTemplate.xml'

#    install location
dir = arcpy.GetInstallInfo("desktop")["InstallDir"] 

#    stylesheet to use
copy_xslt = r"{0}".format(os.path.join(dir,"Metadata\Stylesheets\gpTools\exact copy of.xslt"))

def update_metadata(root):
    num_elements = 0

    # if purpose element does not exist:
    #   import metadata from template
    # if element exists, do nothing
    purposeEls = root.findall(".//idPurp")
    if not purposeEls:
        print filename + ': No //idPurp tag'
        
        #ImportMetadata_conversion (Source_Metadata, Import_Type, Target_Metadata, Enable_automatic_updates)
        arcpy.ImportMetadata_conversion (sourceMeatadata ,"FROM_ARCGIS",filename)

    else:
        for element in purposeEls:
            print filename # + ": " + element.text




#for item in datasetList:
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        feature_classes.append(filename)

        #    temporary XML file
        xmlfile = arcpy.CreateScratchName(".xml",workspace=arcpy.env.scratchFolder)
    
        # export xml
        arcpy.XSLTransform_conversion(filename, copy_xslt, xmlfile, "")
    
        # read in XML
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        #changes = update_metadata(root)
        update_metadata(root)
    
#arcpy.AddMessage('Finished updating metadata for all source metadata items')
print 'Finished updating metadata for all source metadata items'