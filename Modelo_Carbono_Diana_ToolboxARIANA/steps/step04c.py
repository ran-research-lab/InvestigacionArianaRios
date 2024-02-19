import arcpy
from sys import argv
from datetime import datetime


OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"
output_directory = OUTPUT_GDB + r"\Model4cOutput"
output_directory_raster = OUTPUT_GDB



RootCarbonFinal_4_= OUTPUT_GDB + r"\Model4bOutput\RootCarbonFinal"
RootCarbon= OUTPUT_GDB + r"\Model3cOutput\RootCarbon"


def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))

def step04c(RootCarbonFinal_4_, RootCarbon, output_directory, output_directory_raster):  # 4c Pre-event Root Carbon Calculation_rev
    startTime = datetime.now()

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff", snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):

        # Process: Add Field (2) (Add Field) (management)
        RootCarbon_2_ = arcpy.management.AddField(in_table=RootCarbon, field_name="RootC_Mgh", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField RootC_Mgh", "", startTime)


        # Process: Calculate Field (2) (Calculate Field) (management)
        RootCarbon_3_ = arcpy.management.CalculateField(in_table=RootCarbon_2_, field="RootC_Mgh", expression="notNull(!RootCarb_table_MEAN!)", expression_type="PYTHON3", code_block="def notNull(x): \n  if x: return  x / 100", field_type="TEXT")[0]
        printStatus("CalculateField RootC_Mgh", "", startTime)

        # Process: Add Field (3) (Add Field) (management)
        RootCarbon_4_ = arcpy.management.AddField(in_table=RootCarbon_3_, field_name="RootC_Mg", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField RootC_Mg", "", startTime)

        
        # Add a new field for area in VegElevHill_2_
        arcpy.management.AddField(RootCarbon_4_, "F_AREA", "DOUBLE")
        printStatus("AddField F_AREA", "", startTime)

        # Calculate the area for each feature in VegElevHill_2_
        arcpy.management.CalculateField(RootCarbon_4_, "F_AREA", "!SHAPE.area!", "PYTHON3")
        printStatus("CalculateField F_AREA", "", startTime)

        # Process: Calculate Areas (Calculate Areas) (stats)
        RootCarbon_Area = output_directory + r"\RootCarbon_Area"
        arcpy.management.CopyFeatures(RootCarbon_4_, RootCarbon_Area)
        printStatus("CopyFeatures", RootCarbon_Area, startTime)

        # Process: Calculate Field (3) (Calculate Field) (management)
        RootCarbon_Area_2_ = arcpy.management.CalculateField(in_table=RootCarbon_Area, field="RootC_Mg", expression="notNull(!RootC_Mgh! , !F_AREA!)", expression_type="PYTHON3", code_block="def notNull(x,y): \n  if x:\n    if y: return  x*y/10000 ", field_type="TEXT")[0]
        printStatus("CalculateField RootC_Mg", "", startTime)

        # Process: Select (2) (Select) (analysis)
        RootStreamCarbon = output_directory + r"\RootStreamCarbon"
        arcpy.analysis.Select(in_features=RootCarbon_Area_2_, out_feature_class=RootStreamCarbon, where_clause="StrmHillElev_StrOrder > 0")
        printStatus("Select StrmHillElev_StrOrder > 0", "", startTime)

        # Process: Calculate Field (4) (Calculate Field) (management)
        RootStreamCarbon_2_ = arcpy.management.CalculateField(in_table=RootStreamCarbon, field="RootC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField RootC_Mg", "", startTime)

        # Process: Update (Update) (analysis)
        RootCarbonFinal = output_directory + r"\RootCarbonFinal"
        arcpy.analysis.Update(in_features=RootCarbon_Area_2_, update_features=RootStreamCarbon_2_, out_feature_class=RootCarbonFinal, keep_borders="BORDERS", cluster_tolerance="")
        printStatus("Update ", str(RootCarbonFinal), startTime)

        # Process: Add Field (4) (Add Field) (management)
        RootCarbonFinal_2_ = arcpy.management.AddField(in_table=RootCarbonFinal, field_name="Elev_m", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField Elev_m", "", startTime)

        # Process: Calculate Field (5) (Calculate Field) (management)
        RootCarbonFinal_3_ = arcpy.management.CalculateField(in_table=RootCarbonFinal_2_, field="Elev_m", expression="!StrmHillElev_gridcode!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField Elev_m", "", startTime)

        # Process: Delete Field (Delete Field) (management)
        RootCarbonFinal_4_ = arcpy.management.DeleteField(in_table=RootCarbonFinal_3_, drop_field=["StrmHillElev_OBJECTID_1", "StrmHillElev_grid_code", "StrmHillElev_Shape_Leng", "RootCarbon_table_OBJECTID", "RootCarbon_table_grid_code", "RootCarbon_table_COUNT", "RootCarbon_table_AREA", "RootCarbon_table_SUM", "BGCarbon_table_OBJECTID", "BGCarbon_table_COUNT", "BGCarbon_table_AREA"])[0]
        printStatus("DeleteFields (END)", "", startTime)

