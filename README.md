# Validation of different interpolation methods with the leave one out method
QGIS Processing Plugin which provides different algorithms to interpolate point shapefiles and validate the result with the leave on out method.

## Information about method
The leave one out method is used to validate the accuracy of interpolations. Reading through literature, one also encounters the terms cross validation and jackknifing. Many times the term cross validation is used when desrcibing and using the metod of this plugin in scientific papers. Because of potential condusion between the widely used terms of cross validation and jackknifing this plugin is only names as leave one out method because this describes the method in its core the best. The last section features some publications that were read through while getting into the topic a bit more. This plugin offers algorithms to run and validate different deterministic interpolation methods of QGIS with the leave one out method. 

Therefore the code runs the interpolation method for the whole data set and afterwards does the validation. Resulting, the user gets a text file with the relevant validation data. During the leave one out validation one data point of the input data is removed. Afterwards the interpolation is used on the resulting data with the same parameters. The interpolation result of the validation step is compared to the known, true value of the removed data point. This difference in estimated value and true value (residue) is saved to the validation text file. This procedure is repeated until all data points are validated once. The resulting text file then contains general information about the interpolation method, their parameters, the first column of the attribute rable of the data to associate the data to the input shapefile, the coordinates of the validated point feature as well as the true value, the estimated value of the validation interpolation and the residue.

The user can use the resulting validation residues to calculate statistic parameters like the RMSE to judge the accuracy of the interpolation. At the same time the text file can be used to add the data to QGIS again.

## Included interpolation methods (for now)
* SAGA module thin plate spline (tin)
* SAGA module thin plate spline
* SAGA module interpolate (cubic spline)

## Information/Tipps for the use of the plugin
* open the python console in QGIS while running the plugin to properly see the progress. At the same time this is used to document all the created geodatafiles. SO with this in information you can check if everything went as intended.
* always check, that you actively define the output for the interpolated raster. Becuase SAGA modules result in .sdat files, you either have to actively define that you want to save it as a temporary file or define your output directory with the data file ending. sdat.
* The number 999999.999 in the delta field represents that there was no value to calculate. That means that the data point that was removed was not in the interpolated area of the validation. Therefore no residue value (delta) can be calculated. It was the choice to assign the value 999999.999 instead of a string 'NaN - data point not in the interpolated area', because it makes it easier to import the resulting .txt file into QGIS afterwards. This means with the value, the import will instantly be a number instead of a string field. Therefore it's faster to process with the data afterwards.
* generally keep in mind that NaN values can result because of the way the inteprolation works. For example, cubic spline defines the extent of their interpolation through the data put into the interpolation. That means, that validation of data points at the edge of the data set may result in an interpolation validation raster shape that might not include the removed data point. Therefore a residue is not calculatable.


## Incorporate the Plugin into your QGIS
to be written, either from the repository (if uploaded) or from GitHub

GitHub:
* download the code
* unpack the zip folder and only use the 'IntValidation_leaveoneout' folder
* place the folder in your plugin path that sits in your active profile folder
* start QGIS and activate the Plugin in your extensions
* if everything worked that a new entry should pop up in your Toolbox called 'Leave one out Validation'


Thanks to @jrenken for giving me a lot of helpful tipps to learn python programming in Qgis. Big thanks to @ghtmtt for helping me throughout the learning process, with file structuring, giving tipps and answering all the questions I had very informatively.

## Literature
* Davis, B.M.(1987): Uses and Abuses of Cross-Validationin Geostatistics; Mathematical Geology, 19(3):241-248.
* Tomczak, M.(1998): Spatial Inteprolation and its Uncertainty Using Automated Anisotropic Inverse Distance Weighting (IDW) - Cross-Validation/Jackknifing Approach; Journal of Geographic Information and Decision Analysis, 2(2):18-30.
* Falivene, O.; Cabrera, L.; Tolosana-Delgado, R.; Sáez, A.(2010): Interpolation algorithm ranking using cross-validation and the role of smoothing effect. A coal zone example; Computer & Geoscience, 36:512-519.
* Wise, S.(2011): Cross-validation as a means of investigating DEM interpolation error; Computer & Geoscience, 37:978-991.
* Qiao, P.; Li, P.; Cheng, Y.; Wei, W.; Yang, S.; Lei, M.; Chen, T.(2019): Comparison of common spatial interpolation methods for analysing pollutant spatial distributions at contaminated sites; Environemtal Geochemistry and Health, 41:2709-2730.