
import arcpy
from arcpy.sa import *
from sys import argv
from datetime import datetime


OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"


output_directory = OUTPUT_GDB + r"\Model3dOutput"
output_directory_raster = OUTPUT_GDB

litter_C_log_final=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Datos_Carbono\BioclimClipPRSLM_V1_sa_units800.gdb\litter_C_log_final"
StrmHillElev= OUTPUT_GDB +r"\Model2Output\StrmHillElev"


def printStatus(stage, outFile, startTime):
  print("Done with %s: %s" % (stage, datetime.now()))
  if (len(outFile)>1):
    print("\tOutput file: %s" % outFile)
  print("\tElapsed: %s" % str(datetime.now() - startTime))

def step03d(litter_C_log_final, StrmHillElev, output_directory, output_directory_raster):  # 3d_Extraction of Litter Carbon data
    startTime = datetime.now()
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
        # Process: Make Feature Layer (Make Feature Layer) (management)
        StrmHillElev_Layer = "StrmHillElev_Layer3"
        arcpy.management.MakeFeatureLayer(in_features=StrmHillElev, out_layer=StrmHillElev_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_Elevation_RioHondo FID_Elevation_RioHondo VISIBLE NONE;Id Id VISIBLE NONE;gridcode gridcode VISIBLE NONE;HydroID HydroID VISIBLE NONE;GridID GridID VISIBLE NONE;NextDownID NextDownID VISIBLE NONE;OBJECTID_1 OBJECTID_1 VISIBLE NONE;arcid arcid VISIBLE NONE;grid_code grid_code VISIBLE NONE;from_node from_node VISIBLE NONE;to_node to_node VISIBLE NONE;DrainID DrainID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;StrOrder StrOrder VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")
        printStatus("MakeFeatureLayer", StrmHillElev_Layer, startTime)


        # Process: Raster Calculator (Raster Calculator) (sa)
        LitterCarbon100 = output_directory_raster + r"\LitterCarbon100"
        Raster_Calculator = LitterCarbon100
        litter_C_log_final_raster = Raster(litter_C_log_final)
        LitterCarbon100 = litter_C_log_final_raster * 100
        LitterCarbon100.save(Raster_Calculator)
        printStatus("Raster_Calculator", LitterCarbon100, startTime)



        # Process: Int (Int) (sa)
        LitterCarbon100Int = output_directory_raster + r"\LitterCarbon100Int"
        Int = LitterCarbon100Int
        LitterCarbon100Int = arcpy.sa.Int(in_raster_or_constant=LitterCarbon100)
        LitterCarbon100Int.save(Int)
        printStatus("arcpy.sa", LitterCarbon100Int, startTime)



        # Process: Build Raster Attribute Table (Build Raster Attribute Table) (management)
        LitterCarbon_clip_ha_int_2_ = arcpy.management.BuildRasterAttributeTable(in_raster=LitterCarbon100Int, overwrite="NONE")[0]
        printStatus("BuildRasterAttributeTablea", "", startTime)



        # Process: Zonal Statistics as Table (Zonal Statistics as Table) (sa)
        LitterCarbon_table = output_directory_raster + r"\LitterCarbon_table"
        Zonal_Statistics_as_Table_Result = arcpy.sa.ZonalStatisticsAsTable(in_zone_data=StrmHillElev, zone_field="gridcode", in_value_raster=LitterCarbon_clip_ha_int_2_, out_table=LitterCarbon_table, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[])
        printStatus("ZonalStatisticsAsTable", "", startTime)


        # Process: Add Join (Add Join) (management)
        StrmHillElev_Layer_3_ = arcpy.management.AddJoin(in_layer_or_view=StrmHillElev_Layer, in_field="gridcode", join_table=LitterCarbon_table, join_field="gridcode", join_type="KEEP_ALL")[0]
        printStatus("AddJoin", "", startTime)


        # Process: Select (Select) (analysis)
        LitterCarbon = output_directory + r"\LitterCarbon"
        arcpy.analysis.Select(in_features=StrmHillElev_Layer_3_, out_feature_class=LitterCarbon, where_clause="")
        printStatus("Select (end)", "", startTime)
