# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRange,
                       QgsVectorLayer,
                       QgsField,
                       QgsPointXY,
                       QgsFeature,
                       QgsGeometry,
                       QgsFields
                       )
from qgis import processing
# Open OSGEO4W for qgis and type "pip install OSMPythonTools" or "pip3 install OSMPythonTools"
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api


class ParkingFinder(QgsProcessingAlgorithm):
    """
    put info here
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_LAT = 'INPUT_LAT'
    INPUT_LON = 'INPUT_LON'
    INPUT_BUFFER = 'INPUT_BUFFER'
    INPUT_RESULT_COUNT = 'INPUT_RESULT_COUNT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ParkingFinder()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Parking Finder'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Parking Finder')

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Enter coordinates based on WGS84 (ESPG:4326) projection " +
                        "and a buffer range in feet that you would like to search"+ 
                        " for parking. The smaller the buffer, the more accurate the results" +
                        ". The less results desired, the faster the tool runs. \n"+ 
                        "The results will be displayed as a polygon"+
                        " feature layer and also in the log message box. For detailed"+
                        " results check the feature layer, to view just the names and addresses"+
                        " of the lots check the log output. \n" + 
                        "NOTE: due to the high congestion of parking lots in some areas"+
                        " OSM may have trouble running through a large amount of results,"+
                        " in these areas it is recommended to reduce the amount of results"+
                        " you wish to find to prevent unwanted crashing.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # INPUT COORDS
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_LAT,
                self.tr('Latitude Coordinate ( in WGS84 ESPG:4326 ):'),
                QgsProcessingParameterNumber.Double,
                minValue=-90,
                maxValue=90
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_LON,
                self.tr('LON Coordinate ( in WGS84 ESPG:4326 ):'),
                QgsProcessingParameterNumber.Double,
                minValue=-180,
                maxValue=180
            )
        )
        # INPUT BUFFER
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_BUFFER,
                self.tr('Buffer in feet: (maximum is 20000)'),
                QgsProcessingParameterNumber.Double,
                minValue=1,
                maxValue=20000
            )
        )
        # INPUT RESULT COUNT
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_RESULT_COUNT,
                self.tr('Number of Results: (Maximum is 15)'),
                QgsProcessingParameterNumber.Integer,
                minValue=1,
                maxValue=15
            )
        )
        #PARKING RESULTS
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Parking Results')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        ################# Retrieve INPUTS ###################
        lat = self.parameterAsDouble(parameters, self.INPUT_LAT, context)
        lon = self.parameterAsDouble(parameters, self.INPUT_LON, context)
        buffer = self.parameterAsDouble(parameters, self.INPUT_BUFFER, context)
        num_results = self.parameterAsDouble(parameters, self.INPUT_RESULT_COUNT, context)

        
        ############Main search engine process#################
        
        boundBox = [lat-(buffer/364000), lon-(buffer/288200),lat+(buffer/364000),lon+(buffer/288200)] # lat south, lon west, lat north, lon east
        ### OSM Overpass module, search engine
        overpassQuery = overpassQueryBuilder(
                                            bbox=boundBox, 
                                            elementType='way', 
                                            selector=['"amenity"="parking"'],
                                            out = f'body {num_results}'
                                            )
        overpass = Overpass()
        parking = overpass.query(overpassQuery, timeout=10)

        # format of parkingElements is [information about the parking lot, geometry of the parking lot]
        parkingElements= [[each.tags(),each.geometry(),each.id()] for each in parking.elements()]

        # test if no results
        if len(parkingElements) < 1:
            feedback.pushInfo(f'No parking lots found...please change parameters')
            return{}


        ################ ADDING TO MAP ##################
        layer = QgsVectorLayer('Polygon','poly',"memory")
        pr = layer.dataProvider()
        l = parkingElements[0][0]
        nom = Nominatim()
        listResults = []
        
        #attribute prep
        parkingDetails = ["description","access", "building","building:levels","parking","capacity","fee"]
        fields = QgsFields()
        for i in parkingDetails:
            fields.append(QgsField(i, QVariant.String))
        pr.addAttributes(fields)
        layer.updateFields()
        
        #add each result as a feature to output
        features = []
        for i in parkingElements: # each lot
            # i is each result
            
            #first add geometry
            pnts = []
            for point in i[1]['coordinates'][0]: #each point in polygon
                pnts.append(QgsPointXY(point[0],point[1]))
            poly = QgsFeature(fields)
            poly.setGeometry(QgsGeometry.fromPolygonXY([pnts]))
            
            #reverse geocode for description using nominatim
            d = str(nom.query('way/'+str(i[2]),lookup=True).displayName())
            poly['description'] = d
            listResults.append(d)
            
            #get relevant attributes
            for j in parkingDetails[1::]:
                if j in i[0].keys():
                    poly[j] = i[0][j]
            
            features.append(poly)

        pr.addFeatures(features)
        layer.updateExtents()
        layer.updateFields()
        
        #################Create sink (output)#################
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            layer.fields(),
            layer.wkbType(),
            layer.sourceCrs()
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
            
        for feature in layer.getFeatures():
            sink.addFeature(feature)
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        
        
        ################## print results as well ################
        feedback.pushInfo('Here are the lots we found: ')
        [feedback.pushInfo(i+'\n') for i in listResults]
    
        return {}
