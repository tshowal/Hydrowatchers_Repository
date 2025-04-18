"""
imports
"""

import geopandas as gpd
import pandas as pd
import numpy as np

"""
load shapes
"""
#aerial shape boundary
aerial1 =  gpd.read_file("testing_shapes/test_area_1.shp")
aerial1
#aerial flood extent
aerial_flood = gpd.read_file("testing_shapes/flod_extent_aoi1_aerial.shp")
aerial_flood = aerial_flood.to_crs("EPSG:3857")


aerial_flood["area"] = aerial_flood['geometry'].area
aerial_flood = aerial_flood[aerial_flood['area']>=8093.71]

#aerial_flood.to_file('flood_1acre_test.shp')

#our flood extent
flood16 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_16db.shp")
flood16 = flood16.to_crs("EPSG:3857")
flood18 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_18db.shp")
flood18 = flood18.to_crs("EPSG:3857")
flood20 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_20db.shp")
flood20 = flood20.to_crs("EPSG:3857")


"""
percent overlap
"""

intersection16 = gpd.overlay(aerial_flood, flood16, how='intersection')
intersection18 = gpd.overlay(aerial_flood, flood18, how='intersection')
intersection20 = gpd.overlay(aerial_flood, flood20, how='intersection')

# Calculate the area of the intersection
intersection_area16 = intersection16.geometry.area.sum()
intersection_area18 = intersection18.geometry.area.sum()
intersection_area20 = intersection20.geometry.area.sum()

# Calculate the area of the target polygon (polygon_a)
test_area = aerial_flood.geometry.area.sum()
test_area

pct_16 = (intersection_area16 / test_area) * 100
pct_18 = (intersection_area18 / test_area) * 100
pct_20 = (intersection_area20 / test_area) * 100

pct_16
pct_18
pct_20

"""
calculate area of our flood extent
"""
flood_area16 = flood16.geometry.area.sum()
flood_area18 = flood18.geometry.area.sum()
flood_area20 = flood20.geometry.area.sum()

flood_area16 #covers 70% of 5141784.173760725
flood_area18 #covers 65% of 5141784.173760725 
flood_area20 #covers 44% of 5141784.173760725 

"""
extra remaining flood false negatives?
"""
error16 = ((flood_area16-intersection_area16)/(flood_area16))*100
error18 = ((flood_area18-intersection_area18)/(flood_area18))*100
error20 = ((flood_area20-intersection_area20)/(flood_area20))*100

error16 #39%
error18 #38%
error20 #46%

"""
test area 2
"""

"""
load shapes
"""
#aerial shape boundary
aerial2 =  gpd.read_file("testing_shapes/test_area_2.shp")
aerial2
aerial2 = aerial2.to_crs("EPSG:3857")
#aerial flood extent
aerial_flood = gpd.read_file("testing_shapes/flood_extent_aoi2_aerial.shp")
aerial_flood = aerial_flood.to_crs("EPSG:3857")

aerial_flood["area"] = aerial_flood['geometry'].area
aerial_flood = aerial_flood[aerial_flood['area']>=8093.71]
#aerial_flood.to_file('flood_1acre_test2.shp')

#our flood extent
flood16 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_16db.shp")
flood16 = flood16.to_crs("EPSG:3857")
flood18 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_18db.shp")
flood18 = flood18.to_crs("EPSG:3857")
flood20 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_20db.shp")
flood20 = flood20.to_crs("EPSG:3857")


"""
Only use flood polygons that are in the same area we have aerial photos
"""
flood16 = gpd.sjoin(flood16, aerial2[['geometry']], how='left')
flood16 = flood16.dropna()

flood18 = gpd.sjoin(flood18, aerial2[['geometry']], how='left')
flood18 = flood18.dropna()

flood20 = gpd.sjoin(flood20, aerial2[['geometry']], how='left')
flood20 = flood20.dropna()

"""
percent overlap
"""
intersection16 = gpd.overlay(aerial_flood, flood16, how='intersection')
intersection18 = gpd.overlay(aerial_flood, flood18, how='intersection')
intersection20 = gpd.overlay(aerial_flood, flood20, how='intersection')

# Calculate the area of the intersection
intersection_area16 = intersection16.geometry.area.sum()
intersection_area18 = intersection18.geometry.area.sum()
intersection_area20 = intersection20.geometry.area.sum()

# Calculate the area of the target polygon (polygon_a)
test_area = aerial_flood.geometry.area.sum()
test_area

pct_16 = (intersection_area16 / test_area) * 100
pct_18 = (intersection_area18 / test_area) * 100
pct_20 = (intersection_area20 / test_area) * 100

pct_16
pct_18
pct_20

"""
calculate area of our flood extent
"""
flood_area16 = flood16.geometry.area.sum()
flood_area18 = flood18.geometry.area.sum()
flood_area20 = flood20.geometry.area.sum()

flood_area16 #covers 74% of 1788188.9649758004 
flood_area18 #covers 59% of 1788188.9649758004 
flood_area20 #covers 37% of 1788188.9649758004 

"""
extra remaining flood false negatives?
"""
error16 = ((flood_area16-intersection_area16)/(flood_area16))*100
error18 = ((flood_area18-intersection_area18)/(flood_area18))*100
error20 = ((flood_area20-intersection_area20)/(flood_area20))*100

error16 #78%
error18 #71%
error20 #69%
