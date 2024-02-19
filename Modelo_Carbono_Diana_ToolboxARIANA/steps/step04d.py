
import arcpy
from sys import argv
from datetime import datetime

OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"
output_directory = OUTPUT_GDB + r"\Model4dOutput"
output_directory_raster = OUTPUT_GDB

LitterCarbonFinal_4_= OUTPUT_GDB + r"\Model4dOutput\LitterCarbonFinal"
LitterCarbon= OUTPUT_GDB + r"\Model3dOutput\LitterCarbon"


def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))


def step04d(LitterCarbonFinal_4_, LitterCarbon, output_directory, output_directory_raster):  # 4d Pre-event Litter Carbon Calculation_rev
    startTime = datetime.now()


    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff",snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):

        # Process: Add Field (2) (Add Field) (management)
        LitterCarbon_2_ = arcpy.management.AddField(in_table=LitterCarbon, field_name="LitterC_Mgh", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField LitterC_Mgh", "", startTime)


        # Process: Calculate Field (2) (Calculate Field) (management)
        LitterCarbon_3_ = arcpy.management.CalculateField(in_table=LitterCarbon_2_, field="LitterC_Mgh", expression="notNull(!LitterCarbon_table_MEAN!)", expression_type="PYTHON3", code_block="def notNull(x): \n  if x: return  x / 100", field_type="TEXT")[0]
        printStatus("CalculateField LitterC_Mgh", "", startTime)

        # Process: Add Field (3) (Add Field) (management)
        LitterCarbon_4_ = arcpy.management.AddField(in_table=LitterCarbon_3_, field_name="LitterC_Mg", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        printStatus("AddField LitterC_Mg", "", startTime)
        
        # Add a new field for area in VegElevHill_2_
        arcpy.management.AddField(LitterCarbon_4_, "F_AREA", "DOUBLE")
        printStatus("AddField F_AREA", "", startTime)


        # Calculate the area for each feature in VegElevHill_2_
        arcpy.management.CalculateField(LitterCarbon_4_, "F_AREA", "!SHAPE.area!", "PYTHON3")
        printStatus("CalculateField F_AREA", "", startTime)

        # Process: Calculate Areas (Calculate Areas) (stats)
        LitterCarbonArea = output_directory + r"\LitterCarbonArea"
        arcpy.management.CopyFeatures(LitterCarbon_4_, LitterCarbonArea)
        printStatus("CopyFeatures", str(LitterCarbonArea), startTime)

        # Process: Calculate Field (3) (Calculate Field) (management)
        LitterCarbon_Area_2_ = arcpy.management.CalculateField(in_table=LitterCarbonArea, field="LitterC_Mg", expression="notNull(!LitterC_Mgh!,!F_AREA!)", expression_type="PYTHON3", code_block="def notNull(x,y): \n  if x:\n    if y: return  x*y/10000 ", field_type="TEXT")[0]
        printStatus("CalculateField LitterC_Mg", "", startTime)


        # Process: Select (2) (Select) (analysis)
        LitterStreamCarbon = output_directory + r"\LitterStreamCarbon"
        arcpy.analysis.Select(in_features=LitterCarbon_Area_2_, out_feature_class=LitterStreamCarbon, where_clause="StrmHillElev_StrOrder > 0")
        printStatus("Select StrmHillElev_StrOrder > 0", "", startTime)



        # Process: Calculate Field (4) (Calculate Field) (management)
        LitterStreamCarbon_2_ = arcpy.management.CalculateField(in_table=LitterStreamCarbon, field="LitterC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField LitterC_Mg", "", startTime)


        # Process: Update (Update) (analysis)
        LitterCarbonFinal = output_directory + r"\LitterCarbonFinal"
        arcpy.analysis.Update(in_features=LitterCarbon_Area_2_, update_features=LitterStreamCarbon_2_, out_feature_class=LitterCarbonFinal, keep_borders="BORDERS", cluster_tolerance="")
        printStatus("Update outDFeatureClass: " + str(LitterCarbonFinal), "", startTime)


        # Process: Add Field (4) (Add Field) (management)
        LitterCarbonFinal_2_ = arcpy.management.AddField(in_table=LitterCarbonFinal, field_name="Elev_m", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField Elev_m: ", "", startTime)


        # Process: Calculate Field (5) (Calculate Field) (management)
        LitterCarbonFinal_3_ = arcpy.management.CalculateField(in_table=LitterCarbonFinal_2_, field="Elev_m", expression="!StrmHillElev_gridcode!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField Elev_m: ", "", startTime)

        # Process: Delete Field (Delete Field) (management)
        LitterCarbonFinal_4_ = arcpy.management.DeleteField(in_table=LitterCarbonFinal_3_, drop_field=["StrmHillElev_grid_code", "StrmHillElev_Shape_Leng", "LitterCarbon_table_OBJECTID", "LitterCarbon_table_grid_code", "LitterCarbon_table_AREA", "LitterCarbon_table_COUNT", "LitterCarbon_table_SUM", "RootCarbon_table_OBJECTID", "RootCarbon_table_grid_code", "RootCarbon_table_COUNT", "RootCarbon_table_AREA", "RootCarbon_table_SUM", "BGCarbon_table_OBJECTID", "BGCarbon_table_COUNT", "BGCarbon_table_AREA"])[0]

        printStatus("DeleteField (END)", "" , startTime)
