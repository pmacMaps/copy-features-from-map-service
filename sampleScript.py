# You would use this script to run the function to copy map service features

# import module
import copyFeaturesFromService, os

# log file to write messages to
# update path and file name
logFile = r'[path]\[to]\[file]\Results.txt'

# geodatabase to store feature classes in
fgdb = r'[path]\[to]\[file]\Geodata.gdb'

# single email address to send notification to
email = ['johnDoe@emailwebsite.com']
# send email notification to multiple e-mail addresses
email = ['johnDoe@emailwebsite.com', 'jessesjames@outlaw.com', 'allyourbasearebelongtous@evilvillian.biz']

# sample layer - unsecured
portlandHeritageTreesService = r'https://services.arcgis.com/rOo16HdIMeOBI4Mb/arcgis/rest/services/Heritage_Trees_Portland/FeatureServer/0'
# feature class name
portlandHeritageTrees = os.path.join(fgdb, 'PortlandTrees')

# call function on portland trees
copyFeaturesFromService.copyFeaturesFromService(portlandHeritageTreesService,portlandHeritageTrees,logFile,email,False,True)

# sample layer - secured
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