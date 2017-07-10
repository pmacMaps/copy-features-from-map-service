# Copy Features from a Map/Feature Service

This Python script is a module for copying records from a map/feature service to a feature class, using the Esri ArcPy site package.
It is designed to be run as a function and writes messages to a text file.

The script is a re-factor of the [custom tool](https://geonet.esri.com/docs/DOC-6496-download-arcgis-online-feature-service-or-arcgis-server-featuremap-service) built by Jake Skinner from Esri.
To implement this script, you would import this module into another script, where you would call the function.

The following are the parameters for the function:
- URL for the map or feature service you want to copy records from, with the trailing number
- The feature class where you will copy the records to
- The text file you will write messages to
- If the service comes from an ArcGIS Server (True or False), defaults to False
- If the service comes from ArcGIS Online (True or False), defaults to False
- The token URL part of the ArcGIS Server for generating tokens.  This should only be required for secured services. Defaults to ''
- The username for secured services.  Defaults to ''
- The password for secured services. Defaults to ''

Note: This script is currently under development.
