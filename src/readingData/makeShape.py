#python program to demonstare working with ArcGIS Pro cloned environment in an external IDE
#The program will:
# (1) read conflict CSV data for AFG from HDX, 
# (2) parse the CSV contents into a shapefile, and
# (3) render a simple bar chart of event fatalities and dates
#
#Brian Tomaszewski - bmtski@rit.edu
#22 September 2021
#C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3 - default ArcGIS Pro Python
#C:\Users\*your name*\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone - clone of default ArcGIS Pro Python

#import statments - use Conda/ArcGIS Pro Python manager 
import arcpy
import requests
import csv
import sys
import pandas
#will need to install plotly in your python environment
#import plotly
#import plotly.graph_objects as go

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

#AFG conflict CSV data from HDX
#https://data.humdata.org/dataset/ucdp-data-for-afghanistan
#MAIN_CSV_URL = r'https://data.humdata.org/dataset/a5c24c29-5137-411c-ac08-523d8eda5153/resource/8b486c45-bf57-4f40-8816-8b1d91863c91/download/conflict_data_afg.csv'
#https://www.pcr.uu.se/research/ucdp/methodology/

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

# #open CSV file using requests
# #https://requests.readthedocs.io/en/master/
# req = requests.get(MAIN_CSV_URL)
# csv_content = req.content

# #convert the web content to a string
# csv_in_fixed = str(csv_content, 'utf-8')
# #split the string into lines so it can be parsed as CSV
# #https://www.w3schools.com/python/ref_string_splitlines.asp
# lines = csv_in_fixed.splitlines()

# #put the CSV into a dictionary
# datareader = csv.DictReader(lines)
datareader = reading.getDictionary()

#identifier for each record
rowidval = 0

#lists that will go into the plotly bar chart
# event_dates = []
# event_fatalities = []
# event_location = []
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
        
        #add dates for the plot if 1 or more fatalities were found, dates and fatalities will be plotted with ploty
        # if (int(row[CSV_FIELD_EVENT_FATALITIES])) >= 1:
        #     event_dates.append(row[CSV_FIELD_EVENT_DATE])
        #     event_fatalities.append(int(row[CSV_FIELD_EVENT_FATALITIES]))
        #     event_location.append(row[CSV_FIELD_EVENT_LOCATION]) 
        
        
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        #set the row ID back 1 if there was problem
        rowidval -= 1

    del cursor
    
#make a simple chart from the CSV data
#https://plotly.com/python/creating-and-updating-figures/

""" fig = go.Figure(
    data=[go.Bar(x=event_dates, y=event_fatalities)],
    layout=go.Layout(
        title=go.layout.Title(text="AFG Conflict Dates and Fatalities")
    )
)

fig.write_html(ROOT_DIRECTORY + 'dates_and_fatalities.html', auto_open=True) """

print("finished")
