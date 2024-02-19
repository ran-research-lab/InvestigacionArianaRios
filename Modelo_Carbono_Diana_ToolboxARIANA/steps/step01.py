from datetime import datetime
import arcpy
from sys import argv

INPUT_DIR = r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m"

studyAreaDEM = INPUT_DIR + r"\dem15aff" 
demRemapTable = INPUT_DIR + r"\archivos.gdb\dem_reclass_table75m"
chosenWatershed = INPUT_DIR + "\Watershed.shp"

OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"
outputModel = OUTPUT_GDB + r"\Model1Output"
watershedElevation = OUTPUT_GDB + r"\Elevation_RioHondo"

# Given:
# * raster of elevation (dem15aff)
# * remap table
# * a chosen watershed
# Outputs:
# * Elevation Polygon of the watershed area
# * DEM+Poly: elevation of the whole area

def step01(studyAreaDEM, demRemapTable, chosenWatershed, watershedElevation, outputModel):  # 1_DEM Reclass to Elevation Polygon

    print("Started: " + str(datetime.now()))
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", 
                          mask= INPUT_DIR + r"\dem15aff", 
                          snapRaster= INPUT_DIR + r"\dem15aff"):


        # Process: Reclass by Table (Reclass by Table) (sa)
        Reclass_by_Table = outputModel + r"\RioHondo_elevation_75m" 
        DEM_Reclass = arcpy.sa.ReclassByTable(in_raster=studyAreaDEM, in_remap_table=demRemapTable, from_value_field="FROM_", to_value_field="TO", 
                                              output_value_field="OUT", missing_values="DATA")
        DEM_Reclass.save(Reclass_by_Table)
        print("Done with Reclass: " + str(datetime.now()))
        print("Output file:" + Reclass_by_Table)
        

        # Process: Raster to Polygon (Raster to Polygon) (conversion)
        DEM_Polygon_Shapefile = outputModel + r"\DEM_poly"
        arcpy.conversion.RasterToPolygon(in_raster=DEM_Reclass, out_polygon_features=DEM_Polygon_Shapefile, simplify="SIMPLIFY", raster_field="VALUE", 
                                         create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)
        print("Done with Raster to Polygon: " + str(datetime.now()))
        print("Output file:" + DEM_Polygon_Shapefile)
        
        
        # Process: Clip (Clip) (analysis)
        arcpy.analysis.Clip(in_features=DEM_Polygon_Shapefile, clip_features=chosenWatershed, out_feature_class=watershedElevation, cluster_tolerance="")
        print("Done with Clip: " + str(datetime.now()))
        print("Output file:" + watershedElevation)
        
# if __name__ == '__main__':
#     # Global Environment settings
#     with arcpy.EnvManager(scratchWorkspace  =outputModel, workspace= outputModel):
#         step01(studyAreaDEM, demRemapTable, chosenWatershed, watershedElevation,  outputModel)

def funny():
  print("jajacaacaaaaxxxooo")

# output_directory = gdbForOutput + r"\Model2Output"
# output_directory_raster = gdbForOutput

# Chosen_Watershed= baseDir + r"\Watershed_RioHondo.shp"
# Chosen_Watershed_Elevation = gdbForOutput + r"\Elevation_RioHondo"
# StrmHillElev_3_= gdbForOutput + r"\Model2Output\StrmHillElev" 
# Stream_Order=baseDir + r"\StreamT_StreamO1_DL.shp"

# def step02(Chosen_Watershed, Chosen_Watershed_Elevation, StrmHillElev_3_, Stream_Order, output_directory, output_directory_raster):  # 2_4th Order Stream Hillslope Poly

#     timeStart = datetime.now()
#     print("Started: " + str(timeStart))
    
#     # To allow overwriting outputs change overwriteOutput option to True.
#     arcpy.env.overwriteOutput = True

#     # Model Environment settings
#     with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", 
#                           mask=baseDir + r"\dem15aff", 
#                           snapRaster=baseDir + r"\dem15aff"):
#         Sub_Catchment = baseDir + r"\StreamT_StreamO1_DL.shp"

#         # Process: Clip (Clip) (analysis)
#         Subcatchment_Clip = output_directory + r"\subcatchmentclip"
#         arcpy.analysis.Clip(in_features=Sub_Catchment, clip_features=Chosen_Watershed, out_feature_class=Subcatchment_Clip, cluster_tolerance="")
        
#         print("Done with Subcatchment_Clip: " + str(datetime.now()))
#         print("Output file:" + Subcatchment_Clip)
#         print("Elapsed: " + str(datetime.now() - timeStart))
        
#         # Process: Clip (2) (Clip) (analysis)
#         Stream_Order_Clip = output_directory + r"\strmorderclip"
#         arcpy.analysis.Clip(in_features=Stream_Order, clip_features=Chosen_Watershed, out_feature_class=Stream_Order_Clip, cluster_tolerance="")
        
#         print("Done with Stream_Order_Clip: " + str(datetime.now()))
#         print("Output file:" + Stream_Order_Clip)
#         print("Elapsed: " + str(datetime.now() - timeStart))
        
        
#         # Process: Add Field (Add Field) (management)
#         Stream_Order_Clip_2_ = arcpy.management.AddField(in_table=Stream_Order_Clip, field_name="BUFFER", field_type="SHORT", 
#                                                          field_precision=None, field_scale=None, field_length=None, field_alias="", 
#                                                          field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

#         print("Done with Stream_Order_Clip_2_: " + str(datetime.now()))
#         print("Elapsed: " + str(datetime.now() - timeStart))
        
        
#         # Process: Calculate Field (Calculate Field) (management)
#         Stream_Order_Clip_3_ = arcpy.management.CalculateField(in_table=Stream_Order_Clip_2_, field="BUFFER", expression="!GRID_CODE! * 15", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]
       
#         print("Done with Stream_Order_Clip_3_: " + str(datetime.now()))
#         print("Elapsed: " + str(datetime.now() - timeStart))

#         # Process: Buffer (Buffer) (analysis)
#         Stream_Order_Clip_Buffer = output_directory + r"\strmorderclip_Buffer1"
#         arcpy.analysis.Buffer(in_features=Stream_Order_Clip_3_, out_feature_class=Stream_Order_Clip_Buffer, buffer_distance_or_field="BUFFER", line_side="FULL", line_end_type="FLAT", dissolve_option="LIST", dissolve_field=["grid_code"], method="PLANAR")

#         print("Done with Stream_Order_Clip_Buffer: " + str(datetime.now()))
#         print("Output feature class:" + Stream_Order_Clip_Buffer)
#         print("Elapsed: " + str(datetime.now() - timeStart))

        
#         # Process: Select (2) (Select) (analysis)
#         Buffer_3 = output_directory + r"\Buffer3"
#         arcpy.analysis.Select(in_features=Stream_Order_Clip_Buffer, out_feature_class=Buffer_3, where_clause="GRID_CODE = 3")

#         # Process: Select (3) (Select) (analysis)
#         Buffer_4 = output_directory + r"\Buffer4"
#         arcpy.analysis.Select(in_features=Stream_Order_Clip_Buffer, out_feature_class=Buffer_4, where_clause="GRID_CODE = 4")

#         # Process: Erase (2) (Erase) (analysis)
#         Buffer3_4 = output_directory + r"\Buffer3_4"
#         arcpy.analysis.Erase(in_features=Buffer_3, erase_features=Buffer_4, out_feature_class=Buffer3_4, cluster_tolerance="")

#         # Process: Select (5) (Select) (analysis)
#         Buffer_1 = output_directory + r"\Buffer1"
#         arcpy.analysis.Select(in_features=Stream_Order_Clip_Buffer, out_feature_class=Buffer_1, where_clause="GRID_CODE = 1")

#         # Process: Erase (6) (Erase) (analysis)
#         Buffer1_4 = output_directory + r"\Buffer1_4"
#         arcpy.analysis.Erase(in_features=Buffer_1, erase_features=Buffer_4, out_feature_class=Buffer1_4, cluster_tolerance="")

#         # Process: Erase (7) (Erase) (analysis)
#         Buffer134 = output_directory + r"\Buffer134"
#         arcpy.analysis.Erase(in_features=Buffer1_4, erase_features=Buffer3_4, out_feature_class=Buffer134, cluster_tolerance="")

#         # Process: Select (Select) (analysis)
#         Buffer_2 = output_directory + r"\Buffer2"
#         arcpy.analysis.Select(in_features=Stream_Order_Clip_Buffer, out_feature_class=Buffer_2, where_clause="GRID_CODE = 2")

#         # Process: Erase (Erase) (analysis)
#         Buffer2_4 = output_directory + r"\Buffer2_4"
#         arcpy.analysis.Erase(in_features=Buffer_2, erase_features=Buffer_4, out_feature_class=Buffer2_4, cluster_tolerance="")

#         # Process: Erase (5) (Erase) (analysis)
#         Buffer234 = output_directory + r"\Buffer234"
#         arcpy.analysis.Erase(in_features=Buffer2_4, erase_features=Buffer3_4, out_feature_class=Buffer234, cluster_tolerance="")

#         # Process: Erase (11) (Erase) (analysis)
#         Buffer1234 = output_directory + r"\Buffer1234"
#         arcpy.analysis.Erase(in_features=Buffer134, erase_features=Buffer234, out_feature_class=Buffer1234, cluster_tolerance="")

#         # Process: Union (Union) (analysis)
#         BufferUnion = output_directory + r"\BufferUnion"
#         arcpy.analysis.Union(in_features=[[Buffer3_4, ""], [Buffer_4, ""], [Buffer1234, ""], [Buffer234, ""]], out_feature_class=BufferUnion, join_attributes="ALL", cluster_tolerance="", gaps="GAPS")

#         print("Done with Embelecos: " + str(datetime.now()))
#         print("Elapsed: " + str(datetime.now() - timeStart))
        
        
#         # Process: Add Field (2) (Add Field) (management)
#         BufferUnion_2_ = arcpy.management.AddField(in_table=BufferUnion, field_name="StrOrder", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

#         # Process: Calculate Field (2) (Calculate Field) (management)
#         BufferUnion_3_ = arcpy.management.CalculateField(in_table=BufferUnion_2_, field="StrOrder", expression="!GRID_CODE! + !GRID_CODE_1! + !GRID_CODE_12! + !GRID_CODE_12_13!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

#         Subcatchment_Clip_Polygon = output_directory_raster + r"\SubcatchmentClipPolygon"
#         arcpy.FeatureToPolygon_management(in_features=Subcatchment_Clip, out_feature_class=Subcatchment_Clip_Polygon)

#         # Process: Identity (Identity) (analysis)
#         StreamHillslope = output_directory + r"\streamhillslope"
#         arcpy.analysis.Identity(in_features=Subcatchment_Clip_Polygon, identity_features=BufferUnion_3_, out_feature_class=StreamHillslope, join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")
        
#         StreamHillslope_Polygon = output_directory_raster + r"\StreamHillslopePolygon"
#         arcpy.FeatureToPolygon_management(in_features=StreamHillslope, out_feature_class=StreamHillslope_Polygon)

#         # Process: Identity (2) (Identity) (analysis)
#         StreamHillslopeElev = output_directory + r"\StreamHillslopeElev"
#         arcpy.analysis.Identity(in_features=Chosen_Watershed_Elevation, identity_features=StreamHillslope_Polygon, out_feature_class=StreamHillslopeElev, join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")

#         # Process: Select (4) (Select) (analysis)
#         StreamHillslopeElevIdentiy_select2 = output_directory + r"\StreamHillslopeElevIdentiy_select2"
#         arcpy.analysis.Select(in_features=StreamHillslopeElev, out_feature_class=StreamHillslopeElevIdentiy_select2, where_clause="StrOrder > grid_code")

#         # Process: Calculate Field (3) (Calculate Field) (management)
#         StreamHillslopeElevIdentiy_select2_3_ = arcpy.management.CalculateField(in_table=StreamHillslopeElevIdentiy_select2, field="StrOrder", expression="!GRID_CODE!", expression_type="PYTHON", code_block="")[0]

#         # Process: Select (6) (Select) (analysis)
#         treamHillslopeElevIdentiy_select1 = output_directory + r"\treamHillslopeElevIdentiy_select1"
#         arcpy.analysis.Select(in_features=StreamHillslopeElev, out_feature_class=treamHillslopeElevIdentiy_select1, where_clause="grid_code > StrOrder AND StrOrder >0")

#         # Process: Calculate Field (4) (Calculate Field) (management)
#         treamHillslopeElevIdentiy_select1_3_ = arcpy.management.CalculateField(in_table=treamHillslopeElevIdentiy_select1, field="StrOrder", expression="!grid_code!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

#         # Process: Join Field (Join Field) (management)
#         StreamHillslopeElevIdentiy_select2_2_ = arcpy.management.JoinField(in_data=StreamHillslopeElevIdentiy_select2_3_, in_field="grid_code", join_table=treamHillslopeElevIdentiy_select1_3_, join_field="grid_code", fields=["Id", "gridcode", "HydroID", "GridID", "NextDownID", "arcid", "grid_code", "from_node", "to_node", "HydroID_1", "Shape_Leng", "Shape_Le_1", "FID_BufferUnion", "StrOrder", "Shape_Length", "Shape_Area", "Name", "HydroID_12", "Shape_Leng_1"])[0]

#         # Process: Update (Update) (analysis)
#         StrmHillElev = output_directory + r"\StrmHillElev"
#         arcpy.analysis.Update(in_features=StreamHillslopeElev, update_features=StreamHillslopeElevIdentiy_select2_2_, out_feature_class=StrmHillElev, keep_borders="BORDERS", cluster_tolerance="")

#         # Process: Delete Field (Delete Field) (management)
#         StrmHillElev_3_ = arcpy.management.DeleteField(in_table=StrmHillElev, drop_field=["FID_streamhillslope", "FID_subcatchmentclip", "HydroID_1", "GridID_1", "NextDown_1", "Shape_Le_1", "FID_BufferUnion", "FID_Buffer3_4", "grid_code_1", "FID_Buffer1234", "grid_code_12", "FID_Buffer234", "grid_code_12_13", "FID_Buffer4", "grid_code_12_13_14"])[0]

#         print("Finished: " + str(datetime.now()))
#         print("Elapsed: " + str(datetime.now() - timeStart))
    
# # if __name__ == '__main__':
# #     # Global Environment settings
# #     with arcpy.EnvManager(scratchWorkspace=output_directory, 
# #                           workspace=output_directory):
# # #         step02(*argv[1:])
# #         step02(Chosen_Watershed, Chosen_Watershed_Elevation, StrmHillElev_3_, Stream_Order, output_directory, output_directory_raster)



