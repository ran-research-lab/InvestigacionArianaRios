
import arcpy
from arcpy.sa import *
from sys import argv
from datetime import datetime

OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"

output_directory = OUTPUT_GDB + r"\Model4bOutput"
output_directory_raster = OUTPUT_GDB


Chosen_ElevStrmHlls= OUTPUT_GDB + r"\Model2Output\StrmHillElev"
SoilCarbonFinal_5_ = OUTPUT_GDB + r"\Model4bOutput\SoilCarbonFinal"
SoilCarbon=OUTPUT_GDB + r"\SoilCarbon"


def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))

def step04b(Chosen_ElevStrmHlls, SoilCarbonFinal_5_, SoilCarbon, output_directory, output_directory_raster):  # 4b Pre-event Soil Carbon Calculation_rev
    startTime = datetime.now()

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff", snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):

        # Process: Add Field (2) (Add Field) (management)
        SoilCarbon_4_ = arcpy.management.AddField(in_table=SoilCarbon, field_name="SoilC_Mgh", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        printStatus("AddField SoilC_Mgh", "" , startTime)


        # Process: Calculate Field (2) (Calculate Field) (management)
        SoilCarbon_5_ = arcpy.management.CalculateField(in_table=SoilCarbon_4_, field="SoilC_Mgh", expression="notNull(!SoilCarbon_table_MEAN!)", expression_type="PYTHON3", code_block="def notNull(x): \n  if x: return  x / 100", field_type="TEXT")[0]
        printStatus("CalculateField SoilC_Mgh", "", startTime)


        # Process: Identity (Identity) (analysis)
        SoilCarbonPoly = output_directory + r"\SoilCarbonPoly"
        arcpy.analysis.Identity(in_features=Chosen_ElevStrmHlls, identity_features=SoilCarbon_5_, out_feature_class=SoilCarbonPoly, join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")
        printStatus("Identity", "", startTime)


        # Process: Add Field (3) (Add Field) (management)
        SoilCarbonPoly_2_ = arcpy.management.AddField(in_table=SoilCarbonPoly, field_name="SoilC_Mg", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        printStatus("AddField", "SoilC_Mg", startTime)
        
        # Add a new field for area in VegElevHill_2_
        arcpy.management.AddField(SoilCarbonPoly_2_, "F_AREA", "DOUBLE")
        printStatus("AddField F_AREA", "", startTime)

        # Calculate the area for each feature in VegElevHill_2_
        arcpy.management.CalculateField(SoilCarbonPoly_2_, "F_AREA", "!SHAPE.area!", "PYTHON3")
        printStatus("CalculateField area", "", startTime)


        # Process: Calculate Areas (Calculate Areas) (stats)
        SoilCarbonPolyArea = output_directory + r"\SoilCarbonPolyArea"
        arcpy.management.CopyFeatures(SoilCarbonPoly_2_, SoilCarbonPolyArea)
        printStatus("CopyFeatures", SoilCarbonPolyArea, startTime)

        # Process: Calculate Field (3) (Calculate Field) (management)
        SoilCarbonPolyArea_2_ = arcpy.management.CalculateField(in_table=SoilCarbonPolyArea, field="SoilC_Mg", expression="notNull(!SoilC_Mgh!, !F_AREA!)", expression_type="PYTHON3", code_block="def notNull(x,y): \n  if x:\n    if y: return  x*y/10000 ", field_type="TEXT")[0]
        printStatus("CalculateField: notNull(!SoilC_Mgh!, !F_AREA!)", "", startTime)

        # Process: Select (2) (Select) (analysis)
        SoilStreamCarbon = output_directory + r"\SoilStreamCarbon"
        arcpy.analysis.Select(in_features=SoilCarbonPolyArea_2_, out_feature_class=SoilStreamCarbon, where_clause="StrOrder > 0")
        printStatus("Select from " + str(SoilStreamCarbon), "", startTime)


        # Process: Calculate Field (4) (Calculate Field) (management)
        SoilStreamCarbon_2_ = arcpy.management.CalculateField(in_table=SoilStreamCarbon, field="SoilC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField SoilC_Mg", "", startTime)


        # Process: Update (Update) (analysis)
        SoilCarbonFinal = output_directory + r"\SoilCarbonFinal"
        arcpy.analysis.Update(in_features=SoilCarbonPolyArea_2_, update_features=SoilStreamCarbon_2_, out_feature_class=SoilCarbonFinal, keep_borders="BORDERS", cluster_tolerance="")
        printStatus("Update", SoilCarbonFinal, startTime)

        # Process: Add Field (4) (Add Field) (management)
        SoilCarbonFinal_2_ = arcpy.management.AddField(in_table=SoilCarbonFinal, field_name="Elev_m", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField Elev_m", "", startTime)

        # Process: Calculate Field (5) (Calculate Field) (management)
        SoilCarbonFinal_3_ = arcpy.management.CalculateField(in_table=SoilCarbonFinal_2_, field="Elev_m", expression="!gridcode!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
        printStatus("CalculateField gridcode", "", startTime)



        # Process: Delete Field (Delete Field) (management)
        SoilCarbonFinal_5_ = arcpy.management.DeleteField(in_table=SoilCarbonFinal_3_, drop_field=["FID_StrmHillElev", "FID_Elevation_RioHondo75m", "Shape_Leng", "SoilCarbon_table_OBJECTID", "SoilCarbon_table_COUNT", "SoilCarbon_table_AREA", "StrmHillElev_STRM_ORD", "FID_streamhillslope", "GRID_CODE_1", "Soils_clip_AREA", "Soils_clip_PERIMETER", "Soils_clip_SSUELOS_", "Soils_clip_SSUELOS_ID", "Soils_clip_AERA__KM2_", "Soils_clip_ACRES", "Soils_clip_Shape_Leng", "Soils_clip_Shape_Le_1", "SoilCarbon_table_SIMBOLO"])[0]
        printStatus("DeleteField for " + str(SoilCarbonFinal_3_), "", startTime)




