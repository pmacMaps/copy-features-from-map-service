# Copy Features from a Map/Feature Service

This Python script is a module for copying records from a map/feature service to a feature class, using the Esri ArcPy site package.
It is designed to be run as a function and writes messages to a text file.

The script is a re-factor of the [custom tool](https://geonet.esri.com/docs/DOC-6496-download-arcgis-online-feature-service-or-arcgis-server-featuremap-service) built by Jake Skinner from Esri.
To implement this script, you would import this module into another script, where you would call the function.

## Notes

- This script is for use with Python 2.7.x and has been tested with the ArcGIS Desktop 10.3.1 release.
- The requested service must allow for data access for the script to run.  If not, it will produce an error. 
- **sampleScript.py** provides an example of how you would use this script in practice.

## Bad Service E-mail Notification

The [email-bad-service](https://github.com/pmacMaps/copy-features-from-map-service/tree/email-bad-service) branch is a modified version of the script that tests to make sure the map/feature service URL is valid, and if there is an error, you can send an e-mail about the service being down.  It uses a helper module to send the e-mail.

## Parameters for Function

The following are the parameters for the function:
- **service:** URL for the map or feature service you want to copy records from, with the trailing number
- **featureClass:** The feature class where you will copy the records to
- **logFile:** The text file you will write messages to
- **agsServer:** If the service comes from an ArcGIS Server (True or False), defaults to False
- **agolServer:** If the service comes from ArcGIS Online (True or False), defaults to False
- **tokenURLPart:** The token URL part of the ArcGIS Server for generating tokens.  This should only be required for secured services. Defaults to ''
- **username:** The username for secured services.  Defaults to ''
- **password:** The password for secured services. Defaults to ''