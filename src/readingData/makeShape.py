#python program to demonstrate working with ArcGIS Pro cloned environment in an external IDE
#The program will:
# (1) read PDF data, 
# (2) parse the table data it finds
# (3) create a shapefile on the data that it finds
#
#Lachezar Todorov - lxt9427@rit.edu
#24 April 2022

#import statments - use Conda/ArcGIS Pro Python manager 
import arcpy
import sys

from read import reading

#CSV field names - add more field names as need be 
TABLE_FIELD_NAME = "Name"
TABLE_FIELD_LATITUDE = "Latitude"	
TABLE_FIELD_LONGITUDE = "Longitude"	
TABLE_FIELD_CASES = "Cases"
TABLE_FIELD_PERCENT = "Percent"

#Shapefile field names 
SHAPEFILE_FIELD_ID = "Id" #automatically added when the shapefile is created, no need to define
SHAPEFILE_FIELD_EVENT_NAME = "name"
SHAPEFILE_FIELD_EVENT_TYPE = "cases"
SHAPEFILE_FIELD_EVENT_PERCENTAGE = "percent"

## define the shapefile that will be created from the csv data ##
#the directory where various files will be written to, modify for the system this code will run on
ROOT_DIRECTORY = 'C:\\College\\Spring_2022\\GIS_IS\\Geotables\\src\\readingData\\shapeFile\\'

#create a PRJ file so the shapefile references correctly.
#https://pro.arcgis.com/en/pro-app/help/mapping/properties/specify-a-coordinate-system.htm
#uses file IO https://www.w3schools.com/python/python_file_write.asp
WGS_84_Info = r'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
f = open(ROOT_DIRECTORY + "WGS_84.prj", "w")
f.write(WGS_84_Info)
f.close()


arcpy.env.overwriteOutput = True

#https://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm
#https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
Output_Shapefile_FeatureClass = arcpy.CreateFeatureclass_management(ROOT_DIRECTORY , "AFG_Conflict_Event.shp", "POINT","","DISABLED","DISABLED",ROOT_DIRECTORY + "WGS_84.prj")
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_NAME, "TEXT", field_length=255)
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_TYPE, "TEXT", field_length=255)
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_PERCENTAGE, "TEXT", field_length=255)


# get the dictionary from the read.py class
datareader = reading.getDictionary()

#identifier for each record
rowidval = 0

#loop through the contents of the CSV and put the  it into a shapefile
nameArray = datareader[TABLE_FIELD_NAME]
latitudeArray = datareader[TABLE_FIELD_LATITUDE]
longitudeArray = datareader[TABLE_FIELD_LONGITUDE]
casesArray = datareader[TABLE_FIELD_CASES]
percentArray = datareader[TABLE_FIELD_PERCENT]

for x in range(len(nameArray)):

    try:
        #for demonstration purposes, only take the first 1000 records then break out of the loop
        if (rowidval == 1000):
            break
        
        shapefile_fields = [SHAPEFILE_FIELD_ID,SHAPEFILE_FIELD_EVENT_NAME,SHAPEFILE_FIELD_EVENT_TYPE, SHAPEFILE_FIELD_EVENT_PERCENTAGE, 'SHAPE@XY']

        #https://pro.arcgis.com/en/pro-app/arcpy/data-access/insertcursor-class.htm
        cursor = arcpy.da.InsertCursor(Output_Shapefile_FeatureClass, shapefile_fields)
        rowidval += 1
        
        xy = (float(longitudeArray[x]), float(latitudeArray[x]))
        
        cursor.insertRow((rowidval,nameArray[x],casesArray[x],percentArray[x],xy))
        
        
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        #set the row ID back 1 if there was problem
        rowidval -= 1

    del cursor

print("finished")
