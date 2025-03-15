""""
Import all necessary packages
"""
import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 
import pandas as pd

""""
read pre and post flood images
"""
# #preflood_VV = 'vh_decible/preflood_VV_01.tiff'
# preflood_VH = 'vh_decible/preflood_VH_05.tiff'
# #postflood_VV= 'vh_decible/postflood_VV_01.tiff'
# postflood_VH = 'vh_decible/postflood_VH_05.tiff'


# #preflood_VVtiff = rasterio.open(preflood_VV)
# preflood_VHtiff = rasterio.open(preflood_VH)
# #postflood_VVtiff = rasterio.open(postflood_VV)
# postflood_VHtiff = rasterio.open(postflood_VH)

post_dem ='dem_tifs/postflood_dem_04.tiff'
post_dem_tiff = rasterio.open(post_dem)

pre_dem ='dem_tifs/preflood_dem_04.tiff'
pre_dem_tiff = rasterio.open(pre_dem)

# file = 'postflood_VH_05/978e4d3b9fa514c2226680957a48aad4/response.tiff'
# tiff = rasterio.open(file)
""""
code to explore plotting and inspection of tiff files if necessary
"""

#rasterio.plot.show(preflood_VVtiff)

# print(tiff.shape)

# num_bands = tiff.count
# print(f"Number of bands: {num_bands}")

# band_indexes = tiff.indexes
# print(f"Band indexes: {band_indexes}")

# band_dtypes = tiff.dtypes
# print(f"Band data types: {band_dtypes}")

""""
read data from a band example
"""

# # Open the GeoTIFF file
# with rasterio.open(file) as src:
#     # Read a specific band (e.g., band 1)
#     band_number = 1
#     band_data = src.read(band_number)

# band_data

""""
bands to pandas each section is for a different band that has been comented out if not using
"""

#different bands to pandas

# da = rxr.open_rasterio(preflood_VV, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# df_preflood_vv = da[0].to_pandas()
# df_preflood_vv['y'] = df_preflood_vv.index
# df_preflood_vv = pd.melt(df_preflood_vv, id_vars='y')
# df_preflood_vv=df_preflood_vv.rename(columns={'value':'preflood_vv'})
# df_preflood_vv

# da = rxr.open_rasterio(postflood_VV, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# df_postflood_vv = da[0].to_pandas()
# df_postflood_vv['y'] = df_postflood_vv.index
# df_postflood_vv = pd.melt(df_postflood_vv, id_vars='y')
# df_postflood_vv=df_postflood_vv.rename(columns={'value':'postflood_vv'})

# da = rxr.open_rasterio(preflood_VH, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# df_preflood_vh = da[0].to_pandas()
# df_preflood_vh['y'] = df_preflood_vh.index
# df_preflood_vh = pd.melt(df_preflood_vh, id_vars='y')
# df_preflood_vh=df_preflood_vh.rename(columns={'value':'preflood_vh'})

# da = rxr.open_rasterio(postflood_VH, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# df_postflood_vh = da[0].to_pandas()
# df_postflood_vh['y'] = df_postflood_vh.index
# df_postflood_vh = pd.melt(df_postflood_vh, id_vars='y')
# df_postflood_vh=df_postflood_vh.rename(columns={'value':'postflood_vh'})

da = rxr.open_rasterio(post_dem, masked=True)
#da = da.rio.reproject("EPSG:4326")
df_postflood_dem = da[0].to_pandas()
df_postflood_dem['y'] = df_postflood_dem.index
df_postflood_dem = pd.melt(df_postflood_dem, id_vars='y')
df_postflood_dem=df_postflood_dem.rename(columns={'value':'postflood_dem'})

da = rxr.open_rasterio(pre_dem, masked=True)
#da = da.rio.reproject("EPSG:4326")
df_preflood_dem = da[0].to_pandas()
df_preflood_dem['y'] = df_preflood_dem.index
df_preflood_dem = pd.melt(df_preflood_dem, id_vars='y')
df_preflood_dem=df_preflood_dem.rename(columns={'value':'preflood_dem'})

""""
merge data into one single pandas dataframe
"""
# join1= pd.merge(df_postflood_vh, df_postflood_vv, on=['y', 'x'], how='inner')
# join2= pd.merge(df_preflood_vv, df_preflood_vh, on=['y', 'x'], how='inner')
# df = pd.merge(join1,join2, on=['y', 'x'], how='inner')
# df

"""
just doing VH here
"""
df= pd.merge(df_postflood_vh, df_preflood_vh, on=['y', 'x'], how='inner')
df

"""
just doing dem here
"""
df= pd.merge(df_postflood_dem, df_preflood_dem, on=['y', 'x'], how='inner')
df

#test if any values differ
df['difference'] = df['postflood_dem']- df['preflood_dem']
df

df[df['difference']!=0]

df1 = df
df2 = df
df3 = df
df4 = df
df5 = df


df1
df2
df3
df4
df5
df_concat = pd.concat([df1, df2, df3, df4, df5])
df_concat

df_concat.to_csv('01_05_decible_vh.csv')

# import pandas as pd
# da = rxr.open_rasterio(tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# df_preflood_vv = da[0].to_pandas()
# df_preflood_vv['y'] = df_preflood_vv.index
# df_preflood_vv = pd.melt(df_preflood_vv, id_vars='y')
# df_preflood_vv
# df_preflood_vv.to_csv('decible.csv')


# df['prefloodvv-postfloodvv'] = df['preflood_vv'] - df['postflood_vv']
# df

# df['prefloodvh-postfloodvh'] = df['preflood_vh'] - df['postflood_vh']
# df
""""
not sure what to do with the data from here
"""
# import seaborn as sns
# import matplotlib.pyplot as plt

# heatmap_data = df.pivot_table(index='y', columns='x', values='prefloodvh-postfloodvh')

# sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Heatmap of Values')
# plt.show()