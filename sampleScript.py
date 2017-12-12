# You would use this script to run the function to copy map service features

# import module
import copyFeaturesFromService, os
from arcpy import env

# set to True to allow for feature classes to be overwritten
# each time script is run is feature class name is the same
env.overwriteOutput = True

# log file to write messages to
# update path and file name
logFile = r'[path]\[to]\[file]\Results.txt'

# placeholder for messages for log file
logMsg = ''

# geodatabase to store feature classes in
fgdb = r'[path]\[to]\[file]\Geodata.gdb'

# single email address to send notification to
email = ['johnDoe@emailwebsite.com']
# send email notification to multiple e-mail addresses
email = ['johnDoe@emailwebsite.com', 'jessesjames@outlaw.com', 'allyourbasearebelongtous@evilvillian.biz']

# sample layer - unsecured
logMsg += 'Copying US States\n'
# service URL
statesService = r'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/3'
# feature class name
statesFC = os.path.join(fgdb, 'US_States')

# call function on portland trees
copyFeaturesFromService.copyFeaturesFromService(statesService,statesFC,logFile,email,True)

# sample layer - secured
logMsg += '\nCopying Wildfire Response\n'
# based on Esri Leaflet sample - https://esri.github.io/esri-leaflet/examples/arcgis-server-auth.html
wildfireResponseService = r'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire_secure_ac/MapServer/0'
# feature class name
wildfireResponse = os.path.join(fgdb, 'WildfireResponse')
# token URL part
tokenURLPart = r'arcgis/tokens/generateToken'
# username
username = 'user1'
# password
password = 'user1'

# call function
copyFeaturesFromService.copyFeaturesFromService(wildfireResponseService,wildfireResponse,logFile,email,True,False,tokenURLPart,username,password)