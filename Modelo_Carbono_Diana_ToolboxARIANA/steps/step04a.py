
import arcpy
from sys import argv
from datetime import datetime

OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"
output_directory = OUTPUT_GDB + r"\Model4aOutput"
output_directory_raster = OUTPUT_GDB

VegCarbonFinal_4_ = OUTPUT_GDB + r"\Model4aOutput\VegCarbonFinal"
ShootCarbon= OUTPUT_GDB + r"\Model3aOutput\ShootCarbon"
Chosen_StrmHillElev= OUTPUT_GDB + r"\Model2Output\StrmHillElev"

ShootCarb_table=OUTPUT_GDB + r"\ShootCarb_table"

def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))

def step04a(VegCarbonFinal_4_, ShootCarbon, Chosen_StrmHillElev, output_directory, output_directory_raster):  # 4a Pre-event Veg Carbon Calculation_rev
    startTime = datetime.now()

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff",snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):
        
        # Process: Add Field (2) (Add Field) (management)
        ShootCarbon_4_ = arcpy.management.AddField(in_table=ShootCarbon, field_name="VegC_Mgh", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField", ShootCarb_table, startTime)

        
        print("About to do CalculateField in " + str(ShootCarbon_4_))
        # Process: Calculate Field (2) (Calculate Field) (management)
        ShootCarbon_2_ = arcpy.management.CalculateField(in_table=ShootCarbon, 
            field="VegC_Mgh", expression="notNull(!ShootCarb_table_MEAN!)", 
            expression_type="PYTHON3", code_block="def notNull(x): \n  if x: return  x / 100", field_type="TEXT")[0]
        printStatus("CalculateField in " + str(ShootCarbon_4_), "", startTime) 
        


        # Process: Identity (Identity) (analysis)
        VegElevHill = output_directory + r"\VegElevHill"
        arcpy.analysis.Identity(in_features=Chosen_StrmHillElev, identity_features=ShootCarbon_2_, out_feature_class=VegElevHill, join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")
        printStatus("Identity", "", startTime) 

        # Process: Add Field (3) (Add Field) (management)
        VegElevHill_2_ = arcpy.management.AddField(in_table=VegElevHill, field_name="VegC_Mg", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
        printStatus("AddField", "", startTime)

        
        # Add a new field for area in VegElevHill_2_
        arcpy.management.AddField(VegElevHill_2_, "F_AREA", "DOUBLE")
        printStatus("AddField", "", startTime)

        # Calculate the area for each feature in VegElevHill_2_
        arcpy.management.CalculateField(VegElevHill_2_, "F_AREA", "!SHAPE.area!", "PYTHON3")
        printStatus("CalculateField", "", startTime)
        

        # Process: Calculate Areas (Calculate Areas) (stats)
        VegElevHill_poly = output_directory + r"\VegElevHill_poly"
        arcpy.management.CopyFeatures(VegElevHill_2_, VegElevHill_poly)
        printStatus("CopyFeatures", VegElevHill_poly, startTime)

        # Process: Calculate Field (3) (Calculate Field) (management)
        Veg_Carbon_Total = arcpy.management.CalculateField(in_table=VegElevHill_poly, field="VegC_Mg", expression="notNull(!VegC_Mgh!,!F_AREA!)", expression_type="PYTHON", code_block="def notNull(x,y): \n  if x:\n    if y: return  x*y/10000 ", field_type="TEXT")[0]
        printStatus("CalculateField", "" , startTime)

        # Process: Select (2) (Select) (analysis)
        VegStreamCarbon = output_directory + r"\VegStreamCarbon"
        arcpy.analysis.Select(in_features=Veg_Carbon_Total, out_feature_class=VegStreamCarbon, where_clause="StrOrder > 0")

        # Process: Calculate Field (4) (Calculate Field) (management)
        VegStreamCarbon_2_ = arcpy.management.CalculateField(in_table=VegStreamCarbon, field="VegC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Update (Update) (analysis)
        VegCarbonFinal = output_directory + r"\VegCarbonFinal"
        arcpy.analysis.Update(in_features=Veg_Carbon_Total, update_features=VegStreamCarbon_2_, out_feature_class=VegCarbonFinal, keep_borders="BORDERS", cluster_tolerance="")

        # Process: Add Field (4) (Add Field) (management)
        VegCarbonFinal_2_ = arcpy.management.AddField(in_table=VegCarbonFinal, field_name="Elev_m", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (5) (Calculate Field) (management)
        VegCarbonFinal_3_ = arcpy.management.CalculateField(in_table=VegCarbonFinal_2_, field="Elev_m", expression="!gridcode!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Delete Field (Delete Field) (management)
        VegCarbonFinal_4_ = arcpy.management.DeleteField(in_table=VegCarbonFinal_3_, drop_field=["NextDownID", "grid_code", "from_node", "to_node", "StrmHillElev_GridID", "StrmHillElev_NextDownID", "StrmHillElev_arcid", "StrmHillElev_from_node", "StrmHillElev_to_node", "IsTerminal", "Shape_Le_1", "StrmHillElev_IsTerminal", "RiverOrder", "JunctionID", "GroupID", "Tc", "StrmHillElev_DrainID", "StrmHillElev_RiverOrder", "StrmHillElev_Tc"])[0]
        printStatus("DeleteField (END)", "" , startTime)

