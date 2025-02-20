"""
first install necessary imports
may need to run a pip install on machine or create virtual environment
"""
import datetime
import os
import getpass

import matplotlib.pyplot as plt
import numpy as np

from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions
)

"""
connecto to sentinel 1 processing API and create configuration
need client ID and client secret from copernicus dashboard to connect
"""

from sentinelhub import SHConfig


config = SHConfig()
config.sh_client_id = '<client id>'
config.sh_client_secret = '<client secret>'
config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
config.save("cdse")

config = SHConfig("cdse")


"""
create eval script to downolad and grab images of interest

current eval script is the VH decible 0 Gamma
"""

evalscriptVH = """
//VERSION=3
function setup() {
  return {
    input: ["VH", "dataMask"],
    output: [
      { id: "default", bands: 4 },
      { id: "eobrowserStats", bands: 1 },
      { id: "dataMask", bands: 1 },
    ],
  };
}

function evaluatePixel(samples) {
  const value = Math.max(0, Math.log(samples.VH) * 0.21714724095 + 1);
  return {
    default: [value, value, value, samples.dataMask],
    eobrowserStats: [Math.max(-30, (10 * Math.log10(samples.VH)))],
    dataMask: [samples.dataMask],
  };
}
// ---
/*
// displays VH in decibels from -20 to 0
// the following is simplified below
// var log = 10 * Math.log(VH) / Math.LN10;
// var val = Math.max(0, (log + 20) / 20);

return [Math.max(0, Math.log(VH) * 0.21714724095 + 1)];
*/

"""

evalscriptVV = """ 
//VERSION=3 
function setup() { 
  return {
    input: ["VV", "dataMask"], 
    output: [ 
      { id: "default", bands: 4 }, 
      { id: "eobrowserStats", bands: 1 }, 
      { id: "dataMask", bands: 1 }, 
    ], 
  }; 
} 
function evaluatePixel(samples) { 
  const value = Math.max(0, Math.log(samples.VV) * 0.21714724095 + 1); 
  return { 
    default: [value, value, value, samples.dataMask], 
    eobrowserStats: [Math.max(-30, (10 * Math.log10(samples.VV)))], 
    dataMask: [samples.dataMask], 
  }; 
} 
// --- 
/* 
  // displays VV in decibels from -20 to 0 
  // the following is simplified below 
  // var log = 10 * Math.log(VV) / Math.LN10; 
  // var val = Math.max(0, (log + 20) / 20); 
  return [Math.max(0, Math.log(VV) * 0.21714724095 + 1)]; 
*/ 
""" 

"""
send request
"""
# change coordinates by grid request
# copy and pase from excel sheet be sure to include commas between values

#this is changing depending on grid being pulled
bbox1 = BBox(bbox=[-66.4386081, 18.46376767,	-66.3886081,	18.41876767], crs=CRS.WGS84)
bbox2 = BBox(bbox=[-66.3886081,	18.46376767,	-66.3386081,	18.41876767], crs=CRS.WGS84)
bbox3 = BBox(bbox=[-66.3386081,	18.46376767,	-66.2886081,	18.41876767], crs=CRS.WGS84)
bbox4 = BBox(bbox=[-66.2886081,	18.46376767,	-66.2386081,	18.41876767], crs=CRS.WGS84)
bbox5 = BBox(bbox=[-66.2386081,	18.46376767,	-66.1886081,	18.41876767], crs=CRS.WGS84)

size1 = [528.0843937854222, 500.93770856969985]
size2 = [528.0843937852881, 500.93770856969985]
size3 = [528.0843937852881, 500.93770856969985]
size4 = [528.0843937854222, 500.93770856969985]
size5 = [528.0843937852881, 500.93770856969985]

# namming convention
# preflood_VV_gridnumber
# postflood_VV_gridnumber
# preflood_VH_gridnumber
# postflood_VH_gridnumber

#pre flood time: '2017-09-01', '2017-09-16'
#post flood time: '2017-09-20', '2017-09-28'

request = SentinelHubRequest(
    data_folder="postflood_VH_01", #this is changing every pull
    evalscript=evalscriptVH,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL1_IW.define_from(
                    "s1iw", service_url=config.sh_base_url
                ),          
            time_interval=('2017-09-01', '2017-09-16'), #this is chnaging depending on pre or post flood         
            other_args={"dataFilter": {"mosaickingOrder": "mostRecent"},"processing": {"backCoeff": "GAMMA0_TERRAIN","orthorectify": True,"demInstance": "COPERNICUS","speckleFilter": {"type": "LEE","windowSizeX": 3,"windowSizeY": 3}}}
        ),
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
    ],
    bbox=bbox1,
    size=size1,
    config=config
)

request.get_data()

"""
save geotiff to folder
"""

#%%time
layer = request.get_data(save_data=True)
for folder, _, filenames in os.walk(request.data_folder):
    for filename in filenames:
        print(os.path.join(folder, filename))

layer

"""
read geotiff as a dataframe
"""

import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 

file = 'test/85d04f52ed4133d55e72d84a476ef5a6/response.tiff' #file path of the geotiff you saved
#reccomend renaming response.tiff to the naming convention.tiff instead, we can then place all of our tiff images into a shared folder on git hub
tiff = rasterio.open(file)
tiff

with rasterio.open(file) as src:
    # Read a specific band (e.g., band 1)
    band_number = 1
    band_data = src.read(band_number)

band_data

#save it as a pandas data frame

import pandas as pd
da = rxr.open_rasterio(file, masked=True)
#da = da.rio.reproject("EPSG:4326")
df = da[0].to_pandas()
df['y'] = df.index
df = pd.melt(df, id_vars='y')
df


