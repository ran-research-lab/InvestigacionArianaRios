import arcpy
from arcpy.sa import *
from sys import argv

import sys
sys.path.append(r'utils')
# import steps.utils


from datetime import datetime



OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"


output_directory = OUTPUT_GDB + r"\Model3aOutput"
output_directory_raster = OUTPUT_GDB

ShootCarb_table= OUTPUT_GDB + r"\ShootCarb_table"
ShootCarbon = OUTPUT_GDB  + r"\Model3aOutput\ShootCarbon"
shoot_C_log_final=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Datos_Carbono\BioclimClipPRSLM_V1_sa_units800.gdb\shoot_C_log_final" 
StrmHillElev= OUTPUT_GDB + r"\Model2Output\StrmHillElev"

def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))

def step03a(ShootCarb_table, ShootCarbon, shoot_C_log_final, StrmHillElev, output_directory, output_directory_raster):  # 3a_Extraction of Shoot Carbon data

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")
    arcpy.CheckOutExtension("ImageExt")

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", 
        mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff", 
                          snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):

        # 
        timeStart = datetime.now()

        # Process: Make Feature Layer (Make Feature Layer) (management)
        StrmHillElev_Layer = "StrmHillElev_Layer"
        arcpy.management.MakeFeatureLayer(in_features=StrmHillElev, out_layer=StrmHillElev_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_Elevation_RioHondo FID_Elevation_RioHondo VISIBLE NONE;Id Id VISIBLE NONE;gridcode gridcode VISIBLE NONE;HydroID HydroID VISIBLE NONE;GridID GridID VISIBLE NONE;NextDownID NextDownID VISIBLE NONE;OBJECTID_1 OBJECTID_1 VISIBLE NONE;arcid arcid VISIBLE NONE;grid_code grid_code VISIBLE NONE;from_node from_node VISIBLE NONE;to_node to_node VISIBLE NONE;DrainID DrainID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;StrOrder StrOrder VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")
        printStatus("MakeFeatureLayer", StrmHillElev_Layer, datetime.now())
        



        # Process: Raster Calculator (Raster Calculator) (sa)
        ShootC100 = output_directory_raster + r"\ShootC100"
        # Assuming shoot_C_log_final is a path to a raster
        Raster_Calculator = ShootC100
        shoot_C_log_raster = Raster(shoot_C_log_final) # Load the raster
        ShootC100 = shoot_C_log_raster * 100 # Perform the operation
        ShootC100.save(Raster_Calculator) # Save the result

        printStatus("Raster Calculato", Raster_Calculator, timeStart)
        

        # Process: Int (Int) (sa)
        ShootC100int = output_directory_raster + r"\ShootC100int"
        Int = ShootC100int
        ShootC100int = arcpy.sa.Int(in_raster_or_constant=ShootC100)
        ShootC100int.save(Int)

        printStatus("ShootC100int", str(ShootC100int), timeStart)
        

        # Process: Build Raster Attribute Table (Build Raster Attribute Table) (management)
        ShootC100int_2_ = arcpy.management.BuildRasterAttributeTable(in_raster=ShootC100int, overwrite="Overwrite")[0]
        printStatus("BuildRasterAttributeTable", "", timeStart)
        


        # Process: Zonal Statistics as Table (Zonal Statistics as Table) (sa)
        Zonal_Statistics_as_Table_Result = arcpy.sa.ZonalStatisticsAsTable(in_zone_data=StrmHillElev, zone_field="gridcode", in_value_raster=ShootC100int_2_, 
          out_table=ShootCarb_table, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[])
        printStatus("Zonal_Statistics_as_Table_Result", ShootCarb_table, timeStart)
        


        # Zonal_Statistics_as_Table_Result.save(Zonal_Statistics_as_Table)


        # Process: Add Join (Add Join) (management)
        StrmHillElev_Layer_3_ = arcpy.management.AddJoin(in_layer_or_view=StrmHillElev_Layer, in_field="gridcode", 
          join_table=ShootCarb_table, join_field="gridcode", join_type="KEEP_ALL")[0]
        printStatus("StrmHillElev_Layer_3_", "", timeStart)
        

        # Process: Select (Select) (analysis)
        arcpy.analysis.Select(in_features=StrmHillElev_Layer_3_, out_feature_class=ShootCarbon, where_clause="")
        printStatus("Select from " + str(StrmHillElev_Layer_3_), "", timeStart)

        # Process: Delete Field (Delete Field) (management)
        ShootCarbon_3_ = arcpy.management.DeleteField(in_table=ShootCarbon, drop_field=["StrmHillElev_OBJECTID_1", "StrmHillElev_DrainID", "StrmHillElev_FID_Watershed_RioHondo", "StrmHillElev_HydroID_1", "StrmHillElev_HydroID_12", "StrmHillElev_GridID_1", "StrmHillElev_NextDown_1"])[0]
        printStatus("DeleteField from " + str(ShootCarbon), "", timeStart)