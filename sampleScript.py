# You would use this script to run the function to copy map service features

# import module
import copyFeaturesFromService, os
from arcpy import env

# allows feature classes to be overwritten each time data is copied from service
# if not set to True and feature class already exists, an error will be produced
env.overwriteOutput = True

# log file to write messages to
# update path and file name
log_file = r'[path]\[to]\[file]\Results.txt'

# placeholder for messages for text file
log_msg = ''

# geodatabase to store feature classes in
fgdb = r'[path]\[to]\[file]\Geodata.gdb'

# sample layer - unsecured - Pennsylvania Turnpike Plazas
# service URL
turnpike_plaza_service = r'https://maps.pasda.psu.edu/arcgis/rest/services/pasda/PennDOT/MapServer/1'
# feature class name
turnpike_plaza_FC = os.path.join(fgdb, 'PA_Turnpike_Plazas')
# call function on Pennsylvania Turnpike Plazas
copyFeaturesFromService.copyData(turnpike_plaza_service,turnpike_plaza_FC,log_file,True)

# sample layer - secured
# Note: this service produces an error when attempting to copy the records.
# I am including it in the sample simply to show how you would use this module witha  secured service
# based on Esri Leaflet sample - https://esri.github.io/esri-leaflet/examples/arcgis-server-auth.html
wildfire_response_service = r'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire_secure_ac/MapServer/0'
# feature class name
wildfire_response_FC = os.path.join(fgdb, 'WildfireResponse')
# token URL part
token_url_part = r'arcgis/tokens/generateToken'
# username
username = 'user1'
# password
password = 'user1'
# call function on Wildfire Response
copyFeaturesFromService.copyData(wildfire_response_service,wildfire_response_FC,log_file,True,False,token_url_part,username,password)