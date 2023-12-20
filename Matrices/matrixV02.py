import arcpy

# Set the workspace (optional)
arcpy.env.workspace = r'C:\Users\taller\Desktop\ArianaRiosArcGIS\ArianaRiosRectangle\ArianaRiosRectangle\Default.gdb'

# Define the matrix of ones and zeroes (1 = one color, 0 = another color)
matrix = [
    [1, 2, 0, 5],
    [1, 1, 0, 0],
    [0, 0, 2, 1],
    [0, 0, 1, 1]
]

# Create a feature class to store the polygons
output_feature_class = "Polygons"
spatial_reference = arcpy.SpatialReference(4326)  # WGS 84

if arcpy.Exists(output_feature_class):
    arcpy.management.Delete(output_feature_class)

arcpy.management.CreateFeatureclass(arcpy.env.workspace, output_feature_class, "POLYGON", spatial_reference=spatial_reference)

# Create a field to store the color (RGB)
arcpy.AddField_management(output_feature_class, "Value", "Short", field_length=255)

# Create an array to hold polygon vertices
array = arcpy.Array()

# Open an insert cursor for the feature class
with arcpy.da.InsertCursor(output_feature_class, ["SHAPE@", "Value"]) as cursor:
    # Loop through the matrix and create polygons
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value > 0:
                # Add vertices for a square representing one
                x = col_idx
                y = -row_idx  # Invert y-coordinate to match typical Cartesian coordinates
                array.add(arcpy.Point(x, y))
                array.add(arcpy.Point(x + 1, y))
                array.add(arcpy.Point(x + 1, y - 1))
                array.add(arcpy.Point(x, y - 1))

                # Create a polygon geometry using the array of vertices
                polygon = arcpy.Polygon(array)

                # Insert the polygon geometry and color into the feature class
                cursor.insertRow([polygon, value])

                # Clear the array for the next polygon
                array.removeAll()


# Apply symbology from a layer file
layer_file = r"C:\Users\taller\Desktop\ArianaRiosArcGIS\ArianaRiosRectangle\ArianaRiosRectangle\Polygons.lyrx"
arcpy.ApplySymbologyFromLayer_management(output_feature_class, layer_file)

# Print a message to confirm the polygon creation
print("Polygons created successfully.")