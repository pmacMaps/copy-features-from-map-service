# Copy Features from a Map/Feature Service

This Python script is a module for copying records from a map/feature service to a feature class, using the Esri ArcPy site package. It is designed to be run as a function and writes messages to a text file.

The script is a re-factor of the custom tool built by Jake Skinner from Esri. To implement this script, you would import this module into another script, where you would call the function.

This branch includes logic in the function that tests to make sure the map/feature service URL is valid, and if there is an error, you can send an e-mail about the service being down. It uses a helper module to send the e-mail.

The following are the parameters for the function:

- URL for the map or feature service you want to copy records from, with the trailing number
- The feature class where you will copy the records to
- The text file you will write messages to
- The email address to send the alert to
- If the service comes from an ArcGIS Server (True or False), defaults to False
- If the service comes from ArcGIS Online (True or False), defaults to False
- The token URL part of the ArcGIS Server for generating tokens. This should only be required for secured services. Defaults to ''
- The username for secured services. Defaults to ''
- The password for secured services. Defaults to ''
