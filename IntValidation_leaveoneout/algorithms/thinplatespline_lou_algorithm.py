#-*- coding: utf-8 -*-

"""
/***************************************************************************
 InterpolationValidation
                                 A QGIS plugin
 leave one out validation for the interpolation method thinplatespline (tin) from the SAGA console
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-05-23
        copyright            : (C) 2021 by Johannes Ritter
        email                : johannes.ritter95@web.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Johannes Ritter'
__date__ = '2021-05-23'
__copyright__ = '(C) 2021 by Johannes Ritter'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterExtent,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingUtils,
                       QgsRasterLayer,
                       QgsPointXY)

import processing


class ThinplatesplineAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    SHAPES = "SHAPES"
    FIELD = "FIELD"
    REGULARISATION = "REGULARISATION"
    SEARCH_RANGE = "SEARCH_RANGE"
    SEARCH_RADIUS = "SEARCH_RADIUS"
    SEARCH_POINTS_ALL = "SEARCH_POINTS_ALL"
    SEARCH_POINTS_MIN = "SEARCH_POINTS_MIN"
    SEARCH_POINTS_MAX = "SEARCH_POINTS_MAX"
    SEARCH_DIRECTION = "SEARCH_DIRECTION"
    OUTPUT_EXTENT = "OUTPUT_EXTENT"
    TARGET_USER_SIZE = "TARGET_USER_SIZE"
    TARGET_USER_FITS = "TARGET_USER_FITS"
    TARGET_TEMPLATE = "TARGET_TEMPLATE"
    TARGET_OUT_GRID = "TARGET_OUT_GRID"
    INTERPOLATION_RESULT = "INTERPOLATION_RESULT"
    OUTPUT_DATA = "OUTPUT_DATA"

    def initAlgorithm(self, config):

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SHAPES,
                self.tr('Input vector point layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                self.tr('Field to interpolate'),
                "",
                self.SHAPES
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.REGULARISATION,
                self.tr("Regularisation of interpolation"),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0001,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEARCH_RANGE,
                self.tr("Decide for your type of search range"),
                options=[
                    self.tr("[0] local"),
                    self.tr("[1] global")
                ],
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr("Search radius"),
                QgsProcessingParameterNumber.Double,
                defaultValue=1000,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEARCH_POINTS_ALL,
                self.tr("Decide how many points you want to take into account"),
                options=[
                    self.tr("[0] maximum number of nearest points"),
                    self.tr("[1] all points within search area")
                ],
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_POINTS_MIN,
                self.tr("Minimum number of points taken into account"),
                QgsProcessingParameterNumber.Integer,
                defaultValue=16,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_POINTS_MAX,
                self.tr("Maximum number of points (possibly) taken into account"),
                QgsProcessingParameterNumber.Integer,
                defaultValue=20,
                minValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEARCH_DIRECTION,
                self.tr("Search direction"),
                options=[
                    self.tr("[0] all directions"),
                    self.tr("[1] quadrants")
                ],
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
            self.OUTPUT_EXTENT,
            self.tr("Output Extent"),
            optional=1
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TARGET_USER_SIZE,
                self.tr("Cellsize"),
                QgsProcessingParameterNumber.Double,
                defaultValue=100,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.TARGET_USER_FITS,
                self.tr("Fit - where to fit the interpolation to"),
                options=[
                    self.tr("[0] nodes"),
                    self.tr("[1] cells")
                ],
                defaultValue=0
            )
        )

        # add outputs for interpolated raster and validation data
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.INTERPOLATION_RESULT,
                self.tr("Interpolation raster output layer, actively change/chosse the output. Take care that a permanent file must be an .sdat file becuase of the saga module"),
                'sdat files (*.sdat)'
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_DATA,
                self.tr("Output for validation data as .txt file"),
                'txt file (*.txt)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        print("First interpolation starts now, then validation will follow.")
        #instantiating validation text file destination
        #interpolating the surface from the whole data set (int_raster)
        val_txt = self.parameterAsFileOutput(parameters, self.OUTPUT_DATA, context)
        #applying output directory for saga module
        parameters['TARGET_OUT_GRID'] = parameters['INTERPOLATION_RESULT']
        int_raster = processing.run(
            "saga:thinplatespline",
            parameters,
            context=context,
            feedback=feedback
        )
        int_result = int_raster['TARGET_OUT_GRID']

        #instantiating relevant data for validation output data (.txt)
        point_input = self.parameterAsLayer(parameters, self.SHAPES, context)
        int_field = self.parameterAsString(parameters, self.FIELD, context)
        regularisation = self.parameterAsDouble(parameters, self.REGULARISATION, context)
        search_range_type = self.parameterAsEnum(parameters, self.SEARCH_RANGE, context)
        if search_range_type == 0:
            search_range_type = "local"
        elif search_range_type == 1:
            search_range_type = "global"
        search_radius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        points_search_type = self.parameterAsEnum(parameters, self.SEARCH_POINTS_ALL, context)
        if points_search_type == 0:
            points_search_type = "maximum number of nearest points"
        elif points_search_type == 1:
            points_search_type = "all points within search distance"
        minpoints = self.parameterAsInt(parameters, self.SEARCH_POINTS_MIN, context)
        maxpoints = self.parameterAsInt(parameters, self.SEARCH_POINTS_MAX, context)
        search_direction = self.parameterAsEnum(parameters, self.SEARCH_DIRECTION, context)
        if search_direction == 0:
            search_direction = "all directions"
        elif search_direction == 1:
            search_direction = "quadrants"
        extent = self.parameterAsExtent(parameters, self.OUTPUT_EXTENT, context)
        cellsize = self.parameterAsDouble(parameters, self.TARGET_USER_SIZE, context)
        fit = self.parameterAsEnum(parameters, self.TARGET_USER_FITS, context)
        if fit == 0:
            fit = 'nodes'
        elif fit == 1:
            fit = 'cells'
        target_crs = self.parameterAsCrs(parameters, self.TARGET_TEMPLATE, context)
        
        #getting fieldnames of point input layer
        fieldnames = [field.name() for field in point_input.fields()]
        
        #writing the text lines for the validation data text file with intantiated parameters
        gen_info = (
            'Input Layer: {}'.format(point_input.name()),
            str(target_crs),
            'Interpolation field: {}'.format(int_field),
            'Features in input layer: {}'.format(point_input.featureCount())
        )
        int_info = (
            'Interpolation method: SAGA Thin plate spline',
            'Interpolation result path: {}'.format(int_result)
        )
        int_params = (
            'Regularisation: {}'.format(regularisation),
            'Search range type: {}'.format(search_range_type),
            'Search radius: {}'.format(search_radius),
            'points taken into account: {}'.format(points_search_type),
            'min points: {}'.format(minpoints),
            'max points: {}'.format(maxpoints),
            'search direction: {}'.format(search_direction),
            'Output extent (xmin, ymin : xmax, ymax): {}'.format(extent.toString()),
            'Cellsize: {}'.format(cellsize),
            'Interpolation is fit to: {}'.format(fit)
        )
        header = (
            fieldnames[0],
            'x_coord',
            'y_coord',
            int_field,
            'leave one out grid value',
            'd_IntVal(exp)_PoiVal(true)'
        )
        
        #writing information and header into validation text file
        with open(val_txt, 'w') as output_txt:
            line = ';'.join(int_info) + '\n'
            output_txt.write(line)
            line2 = ';'.join(gen_info) + '\n'
            output_txt.write(line2)
            line3 = ';'.join(int_params) + '\n'
            output_txt.write(line3)
            line4 = ';'.join(header) + '\n'
            output_txt.write(line4)
        
        #changing output directory of saga module for validation steps to temporary files
        parameters['TARGET_OUT_GRID'] = QgsProcessing.TEMPORARY_OUTPUT

        features = point_input.getFeatures()
        total = 100.0/point_input.featureCount() if point_input.featureCount() else 0
        
        #loop for validation through every point feature of input layer
        for current, feat in enumerate(features):
            if feedback.isCanceled():
                break
            progress = int(current * total)
            feedback.setProgress(progress)
            if current == 0:
                print("Validation just started")
            else:
                print("Progress of Validation: {}%".format(progress))
            
            #creating a point_clone with the one missing feature to validate
            point_input.select(feat.id())
            point_input.invertSelection()
            tempfile = QgsProcessingUtils.generateTempFilename(str(feat.id())) + '.shp'
            #printing point_clone file location to console
            print("cloned shapefile: {}".format(tempfile))
            poi_clone = processing.run(
                "native:saveselectedfeatures", {
                    'INPUT': point_input,
                    'OUTPUT': tempfile
                }, 
                context=context,
                feedback=feedback
            )['OUTPUT']
            #defining the point_clone as input for the validation interpolation of saga module + running the interpolation with missing feature
            parameters['SHAPES'] = poi_clone
            val_int = processing.run(
                "saga:thinplatespline",
                parameters,
                context=context,
                feedback=feedback
            )
            #printing validation interpolation file path of the point clone to console
            print("validation interpolation of cloned shapefile: {}".format(val_int['TARGET_OUT_GRID']))
            valraster = QgsRasterLayer(
                val_int['TARGET_OUT_GRID'],
                'valint_raster',
                'gdal'
            )
            point_input.removeSelection()

            #accessing field value of missing feature from input layer
            poi_value = feat.attribute(str(int_field))
            geom = feat.geometry()
            #accessing raster value at point of feature from input layer
            valraster_value, res = valraster.dataProvider().sample(
                QgsPointXY(geom.asPoint().x(), geom.asPoint().y()),
                1
            )
            #checking if point is part of raster
            #if so, calculating the delta of expected value (validation interpolation) - true value(input layer feature value)
            if res == False:
                delta = 'NaN - not in interpolated area'
            elif res == True:
                delta = valraster_value - poi_value
            else:
                print('something went horribly wrong here :(')
            
            #writing necessary documentation data + validation delta into validation text data file
            txtdata = (
                str(feat.attribute(0)),
                '{:.4f}'.format(geom.asPoint().x()),
                '{:.4f}'.format(geom.asPoint().y()),
                str(feat.attribute(int_field)),
                str(valraster_value),
                str(delta)
            )
            with open(val_txt, 'a') as output_txt:
                data = ';'.join(txtdata) + '\n'
                output_txt.write(data)
        
        print("The interpolation file: {}".format(int_result))
        print("The validation data in txt file: {}".format(val_txt))
        #returning interpolated raster for data set + validation data set user directories
        return {
            self.INTERPOLATION_RESULT: int_result,
            self.OUTPUT_DATA: val_txt
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Thinplatespline SAGA leave one out validation'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'SAGA LOU validation'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ThinplatesplineAlgorithm()
