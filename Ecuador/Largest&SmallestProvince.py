import arcpy
import os

# Define the input shapefile path
input_class = r"C:\Users\taller\Documents\ArcGIS\Projects\EcuadorShapefile\test.gdb\map.HPLAP-09.13320.12612.sr.lock"

# Get the directory of the input shapefile
output_dir = os.path.dirname(input_class)

# Calculate the areas for each feature and store them in a list
areas = []
with arcpy.da.SearchCursor(input_class, ["SHAPE@", "AREA"]) as cursor:
    for row in cursor:
        shape = row[0]
        area = row[1]
        areas.append((shape, area))

# Sort the list of areas in ascending order
areas.sort(key=lambda x: x[1])

# Get the features with the smallest and largest areas
smallest_feature = areas[0][0]
largest_feature = areas[-1][0]

# Create a new feature class for the smallest area feature
smallest_output = os.path.join(output_dir, "smallest_area2.shp")
arcpy.CopyFeatures_management(smallest_feature, smallest_output)

# Create a new feature class for the largest area feature
largest_output = os.path.join(output_dir, "largest_area2.shp")
arcpy.CopyFeatures_management(largest_feature, largest_output)

print("Process completed. Smallest and largest area shapefiles are saved:")
print("Smallest Area Shapefile:", smallest_output)
print("Largest Area Shapefile:", largest_output)
