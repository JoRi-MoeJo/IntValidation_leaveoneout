# Validation of different interpolation methods with the leave one out method
QGIS Processing Plugin which provides different algorithms to interpolate point shapefiles and validate the result with the leave on out method.

## Information about method
The leave one out method is used to validate the accuracy of interpolations. This plugin offers algorithms to run and validate different deterministic interpolation methods of QGIS with the leave one out method. 
Therefore the code runs the interpolation method for the whole data set and afterwards does the validation. Resulting, the user gets a text file with the relevant validation data. During the leave one out validation one data point of the input data is removed. Afterwards the interpolation is used on the resulting data with the same parameters. The interpolation result of the validation step is compared to the known, true value of the removed data point. This difference in estimated value and true value (residue) is saved to the validation text file. This procedure is repeated until all data points are validated once. The resulting text file then contains general information about the interpolation method, their parameters, the first column of the attribute rable of the data to associate the data to the input shapefile, the coordinates of the validated point feature as well as the true value, the estimated value of the validation interpolation and the residue.
The user can use the resulting validation residues to calculate statistic parameters like the RMSE to judge the accuracy of the interpolation. At the same time the text file can be used to add the data to QGIS again.

## Information for the usage if the plugin
* open the python console in QGIS while running the plugin to properly see the progress. At the same time this is used to document all the created geodatafiles. SO with this in information you can check if everything went as intended.

## Incorporate the PLugin into your QGIS
