import arcpy
from sys import argv
from datetime import datetime


OUTPUT_GDB = r"C:\Users\Rafa\projects\gis\PythonModels.gdb"
output_directory = OUTPUT_GDB + r"\Model5Output"
output_directory_raster = OUTPUT_GDB



Veg_Carbon_Final= OUTPUT_GDB + r"\Model4aOutput\VegCarbonFinal"
Soil_Carbon_Final= OUTPUT_GDB + r"\Model4bOutput\SoilCarbonFinal"
PreEventC_ElevM= OUTPUT_GDB + r"\PreEventC_ElevM"
PreEventC_SStrOrd= OUTPUT_GDB + r"\PreEventC_SStrOrd"
PreEventC_HStrOrd= OUTPUT_GDB + r"\PreEventC_HStrOrd"
PreEventSubcatchmentChannel= OUTPUT_GDB + r"\PreEventSubcatchmentChannel"
PreEventSubcatchHillslope= OUTPUT_GDB + r"\PreEventSubcatchHillslope"
LitterCarbonFinal= OUTPUT_GDB + r"\Model4dOutput\LitterCarbonFinal"
RootCarbonFinal= OUTPUT_GDB + r"\Model4cOutput\RootCarbonFinal"
Watershed_RioHondo_shp=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\Watershed_RioHondo.shp"

def step05(Veg_Carbon_Final, Soil_Carbon_Final, PreEventC_ElevM, PreEventC_SStrOrd, PreEventC_HStrOrd, PreEventSubcatchmentChannel, PreEventSubcatchHillslope, LitterCarbonFinal, RootCarbonFinal, Watershed_RioHondo_shp, output_directory, output_directory_raster):  # 5 Pre-event Combined Carbon stocks_rev

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="526570.079847613 1644641.67664025 661135.079847613 1714721.67664025", mask=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff", 
                          snapRaster=r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\dem15aff"):
        Subcatchment_2_ = r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\Catchment_StreamO1_DL.shp"
        StreamOrder = r"C:\Users\Rafa\projects\gis\Modelo_Carbono_Diana_Data\Landslides_SLM_Red_2018_N\Insumos_Red_2018_N15m\StreamT_StreamO1_DL.shp"

        # Process: Union (2) (Union) (analysis)
        VSRLCarbon = output_directory + r"\VSRLCarbon"
        arcpy.analysis.Union(in_features=[[Soil_Carbon_Final, ""], [Veg_Carbon_Final, ""], [LitterCarbonFinal, ""], [RootCarbonFinal, ""]], out_feature_class=VSRLCarbon, join_attributes="NO_FID", cluster_tolerance="", gaps="GAPS")

        # Process: Delete Field (2) (Delete Field) (management)
        VSRLCarbon_2_ = arcpy.management.DeleteField(in_table=VSRLCarbon, drop_field=["FID_Elevation_RioHondo", "gridcode", "FID_SoilCarbon", "StrmHillElev_Id", "StrmHillElev_HydroID", "StrmHillElev_GridID", "StrmHillElev_from_node", "StrmHillElev_to_node", "StrmHillElev_Shape_Leng", "Id_1", "HydroID_1", "GridID_1", "arcid_1", "Shape_Leng", "FID_ShootCarbon", "StrmHillElev_Id_1", "StrmHillElev_HydroID_1", "StrmHillElev_grid_code_1", "StrmHillElev_Shape_Leng_1", "ShootCarb_table_grid_code", "StrmHillElev_Id_12", "StrmHillElev_gridcode_12", "StrmHillElev_HydroID_12", "StrmHillElev_GridID_1", "StrmHillElev_NextDownID_1", "StrmHillElev_OBJECTID_12", "StrmHillElev_arcid_1", "StrmHillElev_from_node_1", "StrmHillElev_to_node_1", "StrmHillElev_DrainID_1", "StrmHillElev_Id_12_13", "StrmHillElev_gridcode_12_13", "StrmHillElev_HydroID_12_13", "StrmHillElev_GridID_12", "StrmHillElev_arcid_12", "StrmHillElev_from_node_12", "StrmHillElev_to_node_12", "StrmHillElev_Shape_Le_1", "StrmHillElev_Shape_Le_12", "ShootCarb_table_COUNT", "StrmHillElev_HydroID_12_13_14_15", "StrmHillElev_GridID_12_13", "StrmHillElev_NextDown_12", "StrmHillElev_Shape_Le_12_13", "FID_streamhillslope", "FID_subcatchmentclip", "StrmHillElev_Join_Count", "StrmHillElev_TARGET_FID", "StrmHillElev_IsTerminal", "StrmHillElev_STRM_ORD", "SoilCarbon_table_OBJECTID", "FID_StrmHillElev_1", "Join_Count", "TARGET_FID", "STRM_ORD", "StrmHillElev_Join_Count_1", "StrmHillElev_STRM_ORD_1", "StrmHillElev_Join_Count_12", "StrmHillElev_TARGET_FID_1", "StrmHillElev_IsTerminal_1", "StrmHillElev_STRM_ORD_12", "StrmHillElev_Join_Count_12_13", "StrmHillElev_TARGET_FID_12", "StrmHillElev_IsTerminal_12", "StrmHillElev_STRM_ORD_12_13"])[0]
        
        # Add a new field for area in VegElevHill_2_
        arcpy.management.AddField(VSRLCarbon_2_, "F_AREA", "DOUBLE")

        # Calculate the area for each feature in VegElevHill_2_
        arcpy.management.CalculateField(VSRLCarbon_2_, "F_AREA", "!SHAPE.area!", "PYTHON3")

        # Process: Calculate Areas (2) (Calculate Areas) (stats)
        VSRLCarbonFinal = output_directory + r"\VSRLCarbonFinal"
        arcpy.management.CopyFeatures(VSRLCarbon_2_, VSRLCarbonFinal)

        # Process: Calculate Field (Calculate Field) (management)
        VSRLCarbonFinal_2_ = arcpy.management.CalculateField(in_table=VSRLCarbonFinal, field="VegC_Mg", expression="!VegC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (2) (Calculate Field) (management)
        VSRLCarbonFinal_3_ = arcpy.management.CalculateField(in_table=VSRLCarbonFinal_2_, field="SoilC_Mg", expression="!SoilC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (13) (Calculate Field) (management)
        VSRLCarbonFinal_4_ = arcpy.management.CalculateField(in_table=VSRLCarbonFinal_3_, field="RootC_Mg", expression="!RootC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (14) (Calculate Field) (management)
        VSRLCarbonFinal_5_ = arcpy.management.CalculateField(in_table=VSRLCarbonFinal_4_, field="LitterC_Mg", expression="!LitterC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Select (Select) (analysis)
        StreamVSRLCarbonCalc = output_directory + r"\StreamVSRLCarbonCalc"
        arcpy.analysis.Select(in_features=VSRLCarbonFinal_5_, out_feature_class=StreamVSRLCarbonCalc, where_clause="StrOrder > 0")

        # Process: Calculate Field (3) (Calculate Field) (management)
        StreamVSRLCarbonCalc_2_ = arcpy.management.CalculateField(in_table=StreamVSRLCarbonCalc, field="VegC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (4) (Calculate Field) (management)
        StreamVSRLCarbonCalc_3_ = arcpy.management.CalculateField(in_table=StreamVSRLCarbonCalc_2_, field="SoilC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (15) (Calculate Field) (management)
        StreamVSRLCarbonCalc_6_ = arcpy.management.CalculateField(in_table=StreamVSRLCarbonCalc_3_, field="RootC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (17) (Calculate Field) (management)
        StreamVSRLCarbonCalc_5_ = arcpy.management.CalculateField(in_table=StreamVSRLCarbonCalc_6_, field="LitterC_Mg", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Update (3) (Update) (analysis)
        VSRLCarbonTotal2 = output_directory + r"\VSRLCarbonTotal2"
        arcpy.analysis.Update(in_features=VSRLCarbonFinal_5_, update_features=StreamVSRLCarbonCalc_5_, out_feature_class=VSRLCarbonTotal2, keep_borders="BORDERS", cluster_tolerance="")

        # Process: Add Field (Add Field) (management)
        VSRLCarbonTotal2_2_ = arcpy.management.AddField(in_table=VSRLCarbonTotal2, field_name="TotalC_MG", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (5) (Calculate Field) (management)
        VSRLCarbonTotal2_4_ = arcpy.management.CalculateField(in_table=VSRLCarbonTotal2_2_, field="TotalC_MG", expression="!VegC_Mg! + !LitterC_Mg! + !RootC_Mg! + !SoilC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Make Feature Layer (Make Feature Layer) (management)
        VSRLCarbonTotalLayer = "VSRLCarbonTotalLayer"
        arcpy.management.MakeFeatureLayer(in_features=VSRLCarbonTotal2_4_, out_layer=VSRLCarbonTotalLayer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Id Id VISIBLE NONE;HydroID HydroID VISIBLE NONE;GridID GridID VISIBLE NONE;NextDownID NextDownID VISIBLE NONE;OBJECTID_1 OBJECTID_1 VISIBLE NONE;arcid arcid VISIBLE NONE;grid_code grid_code VISIBLE NONE;from_node from_node VISIBLE NONE;to_node to_node VISIBLE NONE;DrainID DrainID VISIBLE NONE;StrOrder StrOrder VISIBLE NONE;StrmHillElev_FID_Elevation_RioHondo StrmHillElev_FID_Elevation_RioHondo VISIBLE NONE;StrmHillElev_gridcode StrmHillElev_gridcode VISIBLE NONE;StrmHillElev_NextDownID StrmHillElev_NextDownID VISIBLE NONE;StrmHillElev_OBJECTID_1 StrmHillElev_OBJECTID_1 VISIBLE NONE;StrmHillElev_arcid StrmHillElev_arcid VISIBLE NONE;StrmHillElev_grid_code StrmHillElev_grid_code VISIBLE NONE;StrmHillElev_DrainID StrmHillElev_DrainID VISIBLE NONE;StrmHillElev_StrOrder StrmHillElev_StrOrder VISIBLE NONE;SoilCarbon_table_grid_code SoilCarbon_table_grid_code VISIBLE NONE;SoilCarbon_table_COUNT_ SoilCarbon_table_COUNT_ VISIBLE NONE;SoilCarbon_table_MEAN SoilCarbon_table_MEAN VISIBLE NONE;SoilC_Mgh SoilC_Mgh VISIBLE NONE;SoilC_Mg SoilC_Mg VISIBLE NONE;F_AREA F_AREA VISIBLE NONE;Elev_m Elev_m VISIBLE NONE;StrmHillElev_FID_Elevation_RioHondo_1 StrmHillElev_FID_Elevation_RioHondo_1 VISIBLE NONE;StrmHillElev_gridcode_1 StrmHillElev_gridcode_1 VISIBLE NONE;StrmHillElev_StrOrder_1 StrmHillElev_StrOrder_1 VISIBLE NONE;LitterCarbon_table_COUNT_ LitterCarbon_table_COUNT_ VISIBLE NONE;LitterCarbon_table_MEAN LitterCarbon_table_MEAN VISIBLE NONE;LitterC_Mgh LitterC_Mgh VISIBLE NONE;LitterC_Mg LitterC_Mg VISIBLE NONE;F_AREA_1 F_AREA_1 VISIBLE NONE;Elev_m_1 Elev_m_1 VISIBLE NONE;StrmHillElev_FID_Elevation_RioHondo_12 StrmHillElev_FID_Elevation_RioHondo_12 VISIBLE NONE;StrmHillElev_NextDownID_12 StrmHillElev_NextDownID_12 VISIBLE NONE;StrmHillElev_DrainID_12 StrmHillElev_DrainID_12 VISIBLE NONE;StrmHillElev_StrOrder_12 StrmHillElev_StrOrder_12 VISIBLE NONE;RootCarb_table_OBJECTID RootCarb_table_OBJECTID VISIBLE NONE;RootCarb_table_grid_code RootCarb_table_grid_code VISIBLE NONE;RootCarb_table_COUNT_ RootCarb_table_COUNT_ VISIBLE NONE;RootCarb_table_AREA RootCarb_table_AREA VISIBLE NONE;RootCarb_table_MEAN RootCarb_table_MEAN VISIBLE NONE;RootC_Mgh RootC_Mgh VISIBLE NONE;RootC_Mg RootC_Mg VISIBLE NONE;F_AREA_12 F_AREA_12 VISIBLE NONE;Elev_m_12 Elev_m_12 VISIBLE NONE;FID_StrmHillElev FID_StrmHillElev VISIBLE NONE;FID_Elevation_RioHondo_1 FID_Elevation_RioHondo_1 VISIBLE NONE;gridcode_1 gridcode_1 VISIBLE NONE;OBJECTID_12 OBJECTID_12 VISIBLE NONE;DrainID_1 DrainID_1 VISIBLE NONE;StrOrder_1 StrOrder_1 VISIBLE NONE;StrmHillElev_FID_Elevation_RioHondo_12_13 StrmHillElev_FID_Elevation_RioHondo_12_13 VISIBLE NONE;StrmHillElev_StrOrder_12_13 StrmHillElev_StrOrder_12_13 VISIBLE NONE;ShootCarb_table_OBJECTID ShootCarb_table_OBJECTID VISIBLE NONE;ShootCarb_table_COUNT_ ShootCarb_table_COUNT_ VISIBLE NONE;ShootCarb_table_AREA ShootCarb_table_AREA VISIBLE NONE;ShootCarb_table_MEAN ShootCarb_table_MEAN VISIBLE NONE;VegC_Mgh VegC_Mgh VISIBLE NONE;VegC_Mg VegC_Mg VISIBLE NONE;F_AREA_12_13 F_AREA_12_13 VISIBLE NONE;Elev_m_12_13 Elev_m_12_13 VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Shape_length Shape_length VISIBLE NONE;Shape_area Shape_area VISIBLE NONE;TotalC_MG TotalC_MG VISIBLE NONE")

        # Process: Clip (2) (Clip) (analysis)
        Subcatchment_Clip = output_directory + r"\Subcatchment_clip"
        arcpy.analysis.Clip(in_features=Subcatchment_2_, clip_features=Watershed_RioHondo_shp, out_feature_class=Subcatchment_Clip, cluster_tolerance="")

        # Process: Make Feature Layer (3) (Make Feature Layer) (management)
        Subcatchment_Clip_Layer = "Subcatchment_clip_Layer"
        arcpy.management.MakeFeatureLayer(in_features=Subcatchment_Clip, out_layer=Subcatchment_Clip_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;HydroID HydroID VISIBLE NONE;GridID GridID VISIBLE NONE;NextDownID NextDownID VISIBLE NONE;OBJECTID_1 OBJECTID_1 VISIBLE NONE;arcid arcid VISIBLE NONE;grid_code grid_code VISIBLE NONE;from_node from_node VISIBLE NONE;to_node to_node VISIBLE NONE;HydroID_1 HydroID_1 VISIBLE NONE;GridID_1 GridID_1 VISIBLE NONE;NextDown_1 NextDown_1 VISIBLE NONE;DrainID DrainID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;Shape_Le_1 Shape_Le_1 VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Shape_length Shape_length VISIBLE NONE;Shape_area Shape_area VISIBLE NONE")

        # Process: Clip (Clip) (analysis)
        Stream_Order_Clip = output_directory + r"\StreamOrderClip"
        arcpy.analysis.Clip(in_features=StreamOrder, clip_features=Watershed_RioHondo_shp, out_feature_class=Stream_Order_Clip, cluster_tolerance="")

        # Process: Make Feature Layer (2) (Make Feature Layer) (management)
        Stream_Order_Clip_Layer = "streamorderclip_Layer"
        arcpy.management.MakeFeatureLayer(in_features=Stream_Order_Clip, out_layer=Stream_Order_Clip_Layer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;arcid arcid VISIBLE NONE;grid_code grid_code VISIBLE NONE;from_node from_node VISIBLE NONE;to_node to_node VISIBLE NONE;HydroID HydroID VISIBLE NONE;GridID GridID VISIBLE NONE;NextDownID NextDownID VISIBLE NONE;DrainID DrainID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;Shape_length Shape_length VISIBLE NONE")

        # Process: Add Join (Add Join) (management)
        Subcatchment_clip_Layer = arcpy.management.AddJoin(in_layer_or_view=Subcatchment_Clip_Layer, in_field="arcid", join_table=Stream_Order_Clip_Layer, join_field="ARCID", join_type="KEEP_ALL")[0]

        # Process: Select (2) (Select) (analysis)
        HillStreamOrder1 = output_directory + r"\HillStreamOrder1"
        arcpy.analysis.Select(in_features=Subcatchment_clip_Layer, out_feature_class=HillStreamOrder1, where_clause="")

        # Process: Add Field (2) (Add Field) (management)
        HillStreamOrder1_2_ = arcpy.management.AddField(in_table=HillStreamOrder1, field_name="HillStrOrd", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Add Field (3) (Add Field) (management)
        HillStreamOrder1_3_ = arcpy.management.AddField(in_table=HillStreamOrder1_2_, field_name="StrArcID", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (6) (Calculate Field) (management)
        HillStreamOrder1_4_ = arcpy.management.CalculateField(in_table=HillStreamOrder1_3_, field="HillStrOrd", expression="!Subcatchment_clip_grid_code!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (7) (Calculate Field) (management)
        HillStreamOrder1_5_ = arcpy.management.CalculateField(in_table=HillStreamOrder1_4_, field="StrArcID", expression="!Subcatchment_clip_arcid!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Make Feature Layer (4) (Make Feature Layer) (management)
        hillstroderlayer = "HillStreamOrder1_Layer"
        arcpy.management.MakeFeatureLayer(in_features=HillStreamOrder1_5_, out_layer=hillstroderlayer, where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Subcatchment_clip_Shape Subcatchment_clip_Shape VISIBLE NONE;Subcatchment_clip_HydroID Subcatchment_clip_HydroID VISIBLE NONE;Subcatchment_clip_GridID Subcatchment_clip_GridID VISIBLE NONE;Subcatchment_clip_NextDownID Subcatchment_clip_NextDownID VISIBLE NONE;Subcatchment_clip_OBJECTID_1 Subcatchment_clip_OBJECTID_1 VISIBLE NONE;Subcatchment_clip_arcid Subcatchment_clip_arcid VISIBLE NONE;Subcatchment_clip_grid_code Subcatchment_clip_grid_code VISIBLE NONE;Subcatchment_clip_from_node Subcatchment_clip_from_node VISIBLE NONE;Subcatchment_clip_to_node Subcatchment_clip_to_node VISIBLE NONE;Subcatchment_clip_HydroID_1 Subcatchment_clip_HydroID_1 VISIBLE NONE;Subcatchment_clip_GridID_1 Subcatchment_clip_GridID_1 VISIBLE NONE;Subcatchment_clip_NextDown_1 Subcatchment_clip_NextDown_1 VISIBLE NONE;Subcatchment_clip_DrainID Subcatchment_clip_DrainID VISIBLE NONE;Subcatchment_clip_Shape_Leng Subcatchment_clip_Shape_Leng VISIBLE NONE;Subcatchment_clip_Shape_Le_1 Subcatchment_clip_Shape_Le_1 VISIBLE NONE;Subcatchment_clip_Shape_length Subcatchment_clip_Shape_length VISIBLE NONE;Subcatchment_clip_Shape_Area Subcatchment_clip_Shape_Area VISIBLE NONE;StreamOrderClip_OBJECTID StreamOrderClip_OBJECTID VISIBLE NONE;StreamOrderClip_arcid StreamOrderClip_arcid VISIBLE NONE;StreamOrderClip_grid_code StreamOrderClip_grid_code VISIBLE NONE;StreamOrderClip_from_node StreamOrderClip_from_node VISIBLE NONE;StreamOrderClip_to_node StreamOrderClip_to_node VISIBLE NONE;StreamOrderClip_HydroID StreamOrderClip_HydroID VISIBLE NONE;StreamOrderClip_GridID StreamOrderClip_GridID VISIBLE NONE;StreamOrderClip_NextDownID StreamOrderClip_NextDownID VISIBLE NONE;StreamOrderClip_DrainID StreamOrderClip_DrainID VISIBLE NONE;StreamOrderClip_Shape_Leng StreamOrderClip_Shape_Leng VISIBLE NONE;StreamOrderClip_Shape_Length StreamOrderClip_Shape_Length VISIBLE NONE;Shape_length Shape_length VISIBLE NONE;Shape_area Shape_area VISIBLE NONE;HillStrOrd HillStrOrd VISIBLE NONE;StrArcID StrArcID VISIBLE NONE")
        
        arcpy.management.AddField(VSRLCarbonTotalLayer, "HydroID", "LONG")
        
        # Process: Add Join (2) (Add Join) (management)
        VSRLCarbonTotalLayer_2_ = arcpy.management.AddJoin(in_layer_or_view=VSRLCarbonTotalLayer, in_field="HydroID", join_table=hillstroderlayer, join_field="Subcatchment_clip_HydroID", join_type="KEEP_ALL")[0]

        # Process: Select (3) (Select) (analysis)
        VSRLCFinal = output_directory + r"\VSRLCFinal"
        arcpy.analysis.Select(in_features=VSRLCarbonTotalLayer_2_, out_feature_class=VSRLCFinal, where_clause="")

        # Process: Add Field (8) (Add Field) (management)
        VSRLCFinal_2_ = arcpy.management.AddField(in_table=VSRLCFinal, field_name="S_StrOrd", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Add Field (9) (Add Field) (management)
        VSRLCFinal_3_ = arcpy.management.AddField(in_table=VSRLCFinal_2_, field_name="H_StrOrd", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Add Field (13) (Add Field) (management)
        VSRLCFinal_4_ = arcpy.management.AddField(in_table=VSRLCFinal_3_, field_name="AreaSq_M", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (11) (Calculate Field) (management)
        VSRLCFinal_5_ = arcpy.management.CalculateField(in_table=VSRLCFinal_4_, field="AreaSq_M", expression="!VSRLCarbonTotal2_F_AREA!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (16) (Calculate Field) (management)
        VSRLCFinal_6_ = arcpy.management.CalculateField(in_table=VSRLCFinal_5_, field="S_StrOrd", expression="!VSRLCarbonTotal2_StrOrder!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (8) (Calculate Field) (management)
        VSRLCFinal_7_ = arcpy.management.CalculateField(in_table=VSRLCFinal_6_, field="H_StrOrd", expression="!HillStreamOrder1_HillStrOrd!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (9) (Calculate Field) (management)
        VSRLCFinal_8_ = arcpy.management.CalculateField(in_table=VSRLCFinal_7_, field="VSRLCarbonTotal2_SoilC_Mg", expression="!VSRLCarbonTotal2_SoilC_Mgh! * !AreaSq_M! /10000", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (10) (Calculate Field) (management)
        VSRLCFinal_9_ = arcpy.management.CalculateField(in_table=VSRLCFinal_8_, field="VSRLCarbonTotal2_VegC_Mg", expression="!VSRLCarbonTotal2_VegC_Mgh! * !AreaSq_M! /10000", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (18) (Calculate Field) (management)
        VSRLCFinal_10_ = arcpy.management.CalculateField(in_table=VSRLCFinal_9_, field="VSRLCarbonTotal2_RootC_Mg", expression="!VSRLCarbonTotal2_RootC_Mgh! * !AreaSq_M! /10000", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (19) (Calculate Field) (management)
        VSRLCFinal_11_ = arcpy.management.CalculateField(in_table=VSRLCFinal_10_, field="VSRLCarbonTotal2_LitterC_Mg", expression="!VSRLCarbonTotal2_LitterC_Mgh! * !AreaSq_M! /10000", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Calculate Field (12) (Calculate Field) (management)
        VSRLCFinal_12_ = arcpy.management.CalculateField(in_table=VSRLCFinal_11_, field="VSRLCarbonTotal2_TotalC_MG", expression="!VSRLCarbonTotal2_SoilC_Mg! + !VSRLCarbonTotal2_RootC_Mg! + !VSRLCarbonTotal2_LitterC_Mg! + !VSRLCarbonTotal2_VegC_Mg!", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Delete Field (Delete Field) (management)
        VSRLCFinal_13_ = arcpy.management.DeleteField(in_table=VSRLCFinal_12_, drop_field=["VSRLCarbonTotal2_Id", "VSRLCarbonTotal2_NextDownID", "VSRLCarbonTotal2_F_AREA", "VSRLCarbonTotal2_StrmHillElev_HydroID_12_13_14", "VSRLCarbonTotal2_StrmHillElev_HydroID_12_13_14_15_16", "VSRLCarbonTotal2_StrmHillElev_GridID_12_13_14_15", "VSRLCarbonTotal2_StrmHillElev_NextDown_12_13", "VSRLCarbonTotal2_StrmHillElev_DrainID_12", "VSRLCarbonTotal2_FID_StrmHillElev", "VSRLCarbonTotal2_StrmHillElev_Shape_Leng_12", "VSRLCarbonTotal2_StrmHillElev_HydroID_12_13_14_15_16_17", "HillStreamOrder1_OBJECTID", "HillStreamOrder1_Subcatchment_clip_GridID", "HillStreamOrder1_StreamOrderClip_OBJECTID", "HillStreamOrder1_StreamOrderClip_grid_code", "HillStreamOrder1_StreamOrderClip_from_node", "HillStreamOrder1_StreamOrderClip_to_node", "HillStreamOrder1_StreamOrderClip_HydroID", "HillStreamOrder1_StreamOrderClip_GridID", "HillStreamOrder1_StreamOrderClip_NextDownID", "HillStreamOrder1_StreamOrderClip_DrainID", "HillStreamOrder1_StreamOrderClip_Shape_Leng", "VSRLCarbonTotal2_FID_Elevation", "VSRLCarbonTotal2_FID_streamhillslope", "VSRLCarbonTotal2_FID_subcatchmentclip", "VSRLCarbonTotal2_Soils_clip_OBJECTID", "VSRLCarbonTotal2_SoilCarbon_table_OBJECTID", "VSRLCarbonTotal2_SoilCarbon_table_ZONE_CODE", "VSRLCarbonTotal2_VegetationClip_OBJECTID", "HillStreamOrder1_subcatchementclip_HydroID", "HillStreamOrder1_subcatchementclip_GridID", "HillStreamOrder1_subcatchementclip_NextDownID", "HillStreamOrder1_subcatchementclip_FID_", "HillStreamOrder1_subcatchementclip_ARCID", "HillStreamOrder1_subcatchementclip_GRID_CODE", "HillStreamOrder1_subcatchementclip_FROM_NODE", "HillStreamOrder1_subcatchementclip_TO_NODE", "HillStreamOrder1_subcatchementclip_OID_1", "HillStreamOrder1_subcatchementclip_GridID_1", "HillStreamOrder1_subcatchementclip_FROM_NODE_", "HillStreamOrder1_subcatchementclip_TO_NODE_1", "HillStreamOrder1_subcatchementclip_HydroID_1", "HillStreamOrder1_subcatchementclip_NextDown_1", "HillStreamOrder1_subcatchementclip_DrainID", "HillStreamOrder1_subcatchementclip_Shape_Leng", "HillStreamOrder1_StreamOrderClip_OID_", "HillStreamOrder1_StreamOrderClip_FROM_NOD_1", "HillStreamOrder1_StreamOrderClip_TO_NODE_1", "HillStreamOrder1_StreamOrderClip_Shape_Le_1"])[0]

        # Process: Select (6) (Select) (analysis)
        VSRLC_final_800m = output_directory + r"\VSRLC_final_800m"
        arcpy.analysis.Select(in_features=VSRLCFinal_13_, out_feature_class=VSRLC_final_800m, where_clause="VSRLCarbonTotal2_Elev_m >= 825")

        # Process: Add Field (4) (Add Field) (management)
        VSRLC_final_825m_2_ = arcpy.management.AddField(in_table=VSRLC_final_800m, field_name="Flag", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

        # Process: Calculate Field (21) (Calculate Field) (management)
        VSRLCFinal_16_ = arcpy.management.CalculateField(in_table=VSRLC_final_825m_2_, field="Flag", expression="0", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Select (7) (Select) (analysis)
        errors = output_directory + r"\Errors"
        arcpy.analysis.Select(in_features=VSRLCFinal_16_, out_feature_class=errors, where_clause="S_StrOrd > 0 AND H_StrOrd > S_StrOrd")

        # Process: Calculate Field (20) (Calculate Field) (management)
        errors_3_ = arcpy.management.CalculateField(in_table=errors, field="Flag", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT")[0]

        # Process: Update (Update) (analysis)
        VSRLCFinal_updated = output_directory + r"\VSRLCFinal_updated"
        arcpy.analysis.Update(in_features=VSRLC_final_825m_2_, update_features=errors_3_, out_feature_class=VSRLCFinal_updated, keep_borders="BORDERS", cluster_tolerance="")

        # Process: Summary Statistics (Summary Statistics) (analysis)
        arcpy.analysis.Statistics(in_table=VSRLCFinal_updated, out_table=PreEventC_ElevM, statistics_fields=[["VSRLCarbonTotal2_SoilC_Mg", "SUM"], ["VSRLCarbonTotal2_LitterC_Mg", "SUM"], ["VSRLCarbonTotal2_VegC_Mg", "SUM"], ["VSRLCarbonTotal2_RootC_Mg", "SUM"], ["VSRLCarbonTotal2_TotalC_MG", "SUM"], ["AreaSq_M", "SUM"]], case_field=["VSRLCarbonTotal2_Elev_m"])

        # Process: Summary Statistics (2) (Summary Statistics) (analysis)
        arcpy.analysis.Statistics(in_table=VSRLCFinal_updated, out_table=PreEventC_HStrOrd, statistics_fields=[["VSRLCarbonTotal2_VegC_Mg", "SUM"], ["VSRLCarbonTotal2_SoilC_Mg", "SUM"], ["VSRLCarbonTotal2_RootC_Mg", "SUM"], ["VSRLCarbonTotal2_LitterC_Mg", "SUM"], ["VSRLCarbonTotal2_TotalC_MG", "SUM"], ["AreaSq_M", "SUM"]], case_field=["H_StrOrd"])

        # Process: Summary Statistics (3) (Summary Statistics) (analysis)
        arcpy.analysis.Statistics(in_table=VSRLCFinal_updated, out_table=PreEventC_SStrOrd, statistics_fields=[["AreaSq_M", "SUM"], ["VSRLCarbonTotal2_SoilC_Mg", "SUM"], ["VSRLCarbonTotal2_LitterC_Mg", "SUM"], ["VSRLCarbonTotal2_RootC_Mg", "SUM"], ["VSRLCarbonTotal2_VegC_Mg", "SUM"], ["VSRLCarbonTotal2_TotalC_MG", "SUM"]], case_field=["S_StrOrd"])

        # Process: Select (4) (Select) (analysis)
        VSRLCFinalSelectChannel = output_directory + r"\VSRLCFinalSelectChannel"
        arcpy.analysis.Select(in_features=VSRLCFinal_updated, out_feature_class=VSRLCFinalSelectChannel, where_clause="VSRLCarbonTotal2_StrOrder >0")
        
        arcpy.management.AddField(VSRLCFinalSelectChannel, "VSRLCarbonTotal2_GridID", "LONG")

        # Process: Summary Statistics (5) (Summary Statistics) (analysis)
        arcpy.analysis.Statistics(in_table=VSRLCFinalSelectChannel, out_table=PreEventSubcatchmentChannel, statistics_fields=[["VSRLCarbonTotal2_VegC_Mg", "SUM"], ["VSRLCarbonTotal2_SoilC_Mg", "SUM"], ["VSRLCarbonTotal2_RootC_Mg", "SUM"], ["VSRLCarbonTotal2_LitterC_Mg", "SUM"], ["VSRLCarbonTotal2_TotalC_MG", "SUM"], ["AreaSq_M", "SUM"], ["S_StrOrd", "MEAN"]], case_field=["VSRLCarbonTotal2_GridID"])

        # Process: Select (5) (Select) (analysis)
        VSRLCFinal_SelectHillslope = output_directory + r"\VSRLCFinal_SelectHillslope"
        arcpy.analysis.Select(in_features=VSRLCFinal_updated, out_feature_class=VSRLCFinal_SelectHillslope, where_clause="VSRLCarbonTotal2_StrOrder <1")
        
        arcpy.management.AddField(VSRLCFinal_SelectHillslope, "VSRLCarbonTotal2_GridID", "LONG")
        
        # Process: Summary Statistics (6) (Summary Statistics) (analysis)
        arcpy.analysis.Statistics(in_table=VSRLCFinal_SelectHillslope, out_table=PreEventSubcatchHillslope, statistics_fields=[["S_StrOrd", "MIN"], ["AreaSq_M", "SUM"], ["VSRLCarbonTotal2_VegC_Mg", "SUM"], ["VSRLCarbonTotal2_SoilC_Mg", "SUM"], ["VSRLCarbonTotal2_RootC_Mg", "SUM"], ["VSRLCarbonTotal2_LitterC_Mg", "SUM"], ["H_StrOrd", "MEAN"], ["S_StrOrd", "MEAN"]], case_field=["VSRLCarbonTotal2_GridID"])


# (step05.Veg_Carbon_Final, step05.Soil_Carbon_Final, step05.PreEventC_ElevM, step05.PreEventC_SStrOrd, step05.PreEventC_HStrOrd, step05.PreEventSubcatchmentChannel, step05.PreEventSubcatchHillslope, step05.LitterCarbonFinal, step05.RootCarbonFinal, step05.Watershed_RioHondo_shp, step05.output_directory, step05.output_directory_raster)