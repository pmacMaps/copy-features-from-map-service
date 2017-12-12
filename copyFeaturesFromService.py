#-------------------------------------------------------------------------------
# Name:        Copy Features from Map/Feature Service Module
# Purpose:
#
# Author:      Jake Skinner, Esri; Patrick McKinney, Cumberland County GIS
#
# Description: Script based upon map service extract tool developed by Jake
#              Skinner from Esri.  Module contains a function for copying data
#              from map/feature services to a feature class.  If there is an
#              error retreiving the service, you can send an e-mail alert.
#
# Created:     6/14/2017
# Updated:     7/12/2017
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

# import modules
import arcpy, urllib, urllib2, json, os, math, sys, emailModule

# Function to copy features from a map or feature service to a feature class
def copyFeaturesFromService(service, featureClass, logFile, email , agsServer=False, agolServer=False, tokenUrlPart='', username='', password=''):
    """ Function to copy features from a map or feature service to a feature class.
        service = the URL for the map/feature service. You must include the number at the end (/0).
        featureClass = the output location and name of the layer you are copying data to.
        logFile = the text file messages will be written to
        email = a list of e-mail address(es) to send a message to if the service URL is down
        agsServer = set to True if the service is hosted on ArcGIS for Server.
        agolServer = set to True if the service is hostedon ArcGIS Online.
        tokenURLPart = the component of an ArcGIS Server URL for generating tokens. Do not include the preceding '/'.
        You should only need to put in a tokenURLPart variable if using a secured service
        username = the username for a secured service.  Leave blank for unsecured services.
        password = the password for a secured service.  Leave blank for unsecured services.
     """
    try:
        # placeholder for message content
        # messages are added to this variable
        # this variable is written to the log file at the end of the script
        logMsg = ''

        from arcpy import env
        # overwite output
        env.overwriteOutput = 1
        # scratch workspace
        # http://pro.arcgis.com/en/pro-app/tool-reference/environment-settings/scratch-gdb.htm
        env.workspace = env.scratchGDB

        # test if URL is valid
        logMsg += '\nTesting if {} is a valid URL.\n'.format(service)

        try:
            # open service to make sure it is a valid url
            testReq = urllib2.urlopen(service)
        except urllib2.URLError as e:
            logMsg += '\nThere was an error accessing the service.\n'
            logMsg += '\nError: {}\n'.format(str(e))
            # e-mail arguments
            emailSubject = 'Map Service Down'
            emailMessage = 'Your service, {}, appeared to be down when we tried to access it.\n'.format(service)
            emailMessage += '\nError: {}\n'.format(str(e))
            # send email
            emailModule.sendEmail(emailMessage,emailSubject,email)
            # log that e-mail has been sent
            for address in email:
                logMsg += '\n{} has been sent an e-mail about service {} being down\n'.format(address,service)
            # end for

        # service url with '/query' appended
        baseURL = r'{}/query'.format(service)

        # if tokenUrlPart == '', use empty string for token
        if tokenUrlPart == '':
            token = ''
        # if tokenUrlPart != '', generate token from token URL
        else:
            # Generate token for service
            logMsg += '\nGenerating token for service\n'
            # Generate token for ArcGIS Online hosted service
            if agolServer == True:
                try:
                    # base token URL
                    tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
                    # parameters for generating token
                    params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'https://www.arcgis.com'}
                    # make a post request
                    req = urllib2.Request(tokenURL, urllib.urlencode(params))
                    # open URL
                    response = urllib2.urlopen(req)
                    # Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a Python object using this conversion table
                    data = json.load(response)
                    token = data['token']
                except:
                    token = ''
                    pass
            # Generate token for ArcGIS Server hosted service
            if agsServer == True:
                try:
                    server = baseURL.split("//")[1].split("/")[0]
                    # URL part for token generation
                    tokenURL = 'https://{}/{}'.format(server, tokenUrlPart)
                    # parameters for token request
                    params = {'username': username, 'password': password, 'client': 'requestip', 'f': 'pjson'}
                    # make request
                    req = urllib2.Request(tokenURL, urllib.urlencode(params))
                    response = urllib2.urlopen(req)
                    data = json.load(response)
                    token = data['token']
                except:
                    token = ''
                    pass

        # Return largest ObjectID
        params = {'where': '1=1', 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
        req = urllib2.Request(baseURL, urllib.urlencode(params))
        response = urllib2.urlopen(req)
        data = json.load(response)
        try:
            data['objectIds'].sort()
        except EnvironmentError as e:
            tbE = sys.exc_info()[2]
            # Write the line number the error occured to the log file
            logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
            logMsg += '\nError: {}\n'.format(str(e))
        except Exception as e:
            tbE = sys.exc_info()[2]
            # Write the line number the error occured to the log file
            logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
            logMsg += '\nError: {}\n'.format(e.message)

        count = len(data['objectIds'])
        iteration = int(data['objectIds'][-1])
        minOID = int(data['objectIds'][0]) - 1
        OID = data['objectIdFieldName']

        # Copy features from service
        if count < 1000:
            x = iteration
            y = minOID
            where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
            fields ='*'

            query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
            fsURL = baseURL + query
            fs = arcpy.FeatureSet()

            # load service
            try:
                fs.load(fsURL)
            except EnvironmentError as e:
                tbE = sys.exc_info()[2]
                # Write the line number the error occured to the log file
                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                logMsg += '\nError loading features: {}.\n'.format(str(e))
            except Exception as e:
                tbE = sys.exc_info()[2]
                # Write the line number the error occured to the log file
                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                logMsg += '\nError loading features: {}.\n'.format(e.message)

            # Copy features
            logMsg += '\nCopying features with ObjectIDs from {} to {}\n'.format(str(y), str(x))
            # Determine type of workspace for feature class
            desc = arcpy.Describe(os.path.dirname(featureClass))
            if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                featureClass2 = featureClass.split(".")[-1]
                try:
                    arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(featureClass), featureClass2)
                except EnvironmentError as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(str(e))
                except Exception as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(e.message)

            else:
                try:
                    arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(featureClass), os.path.basename(featureClass))
                except EnvironmentError as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(str(e))
                except Exception as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(e.message)

        else:
            newIteration = (math.ceil(iteration/1000.0) * 1000)
            x = minOID + 1000
            y = minOID
            firstTime = 'True'

            while y <= newIteration:
                where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
                fields ='*'

                query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
                fsURL = baseURL + query

                fs = arcpy.FeatureSet()

                try:
                    # load service
                    fs.load(fsURL)

                    if firstTime == 'True':
                        logMsg += '\nCopying features with ObjectIDs from {} to {}\n'.format(str(y), str(x))
                        # Determine type of workspace for feature class
                        desc = arcpy.Describe(os.path.dirname(featureClass))
                        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                            featureClass2 = featureClass.split(".")[-1]
                            try:
                                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(featureClass), featureClass2)
                            except EnvironmentError as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(str(e))
                            except Exception as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(e.message)

                        else:
                            try:
                                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(featureClass), os.path.basename(featureClass))
                            except EnvironmentError as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(str(e))
                            except Exception as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(e.message)

                        firstTime = 'False'
                    else:
                        # Determine type of workspace for feature class
                        desc = arcpy.Describe(os.path.dirname(featureClass))
                        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                            logMsg += '\nCopying features with ObjectIDs from {} to {}\n'.format(str(y), str(x))
                            insertRows = arcpy.da.InsertCursor(featureClass, ["*","SHAPE@"])
                            searchRows = arcpy.da.SearchCursor(fs, ["*","SHAPE@"])
                            for searchRow in searchRows:
                                fieldList = list(searchRow)
                                insertRows.insertRow(fieldList)
                        elif desc.workspaceFactoryProgID == '':
                            logMsg += '\nCopying features with ObjectIDs from {} to {}\n'.format(str(y), str(x))
                            try:
                                arcpy.Append_management(fs, featureClass, "NO_TEST")
                            except EnvironmentError as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(str(e))
                            except Exception as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(e.message)

                        else:
                            logMsg += '\nCopying features with ObjectIDs from {} to {}\n'.format(str(y), str(x))
                            try:
                                arcpy.Append_management(fs, featureClass)
                            except EnvironmentError as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(str(e))
                            except Exception as e:
                                tbE = sys.exc_info()[2]
                                # Write the line number the error occured to the log file
                                logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                                logMsg += '\nError: {}\n'.format(e.message)

                except EnvironmentError as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(str(e))
                except Exception as e:
                    tbE = sys.exc_info()[2]
                    # Write the line number the error occured to the log file
                    logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
                    logMsg += '\nError: {}\n'.format(e.message)

                x += 1000
                y += 1000

        try:
            # clean up
            del searchRow, searchRows, insertRows

        except:
            pass

    except EnvironmentError as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
        logMsg += '\nError: {}\n'.format(str(e))

    except Exception as e:
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        logMsg += '\nFailed at Line %i \n' % tbE.tb_lineno
        logMsg += '\nError: {}\n'.format(e.message)

    finally:
        # write message to log file
        try:
            with open(logFile, 'a') as f:
                f.write(str(logMsg))
        except:
            pass
# copyFeaturesFromService