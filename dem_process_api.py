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
config.sh_client_id = 'sh-ac01828e-eb8f-4ff4-b9de-7630c5312236'
config.sh_client_secret = '2NHA7aykyeBqu3NZnrI7n9eVU5NU8oFb'
config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
config.save("cdse")

config = SHConfig("cdse")


"""
create eval script to downolad and grab images of interest

"""
evalscriptdem = """
//VERSION=3

function setup() {
  return {
    input: [
      {
        bands: ["DEM","dataMask"],                  
      }
    ],
    output: [
      {
        id: "default",
        bands: 2,
        sampleType: "FLOAT32",        
      },    
    ],
    mosaicking: "SIMPLE",
  };
}

function evaluatePixel(sample) {
  return [sample.DEM]
}

"""

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
    data_folder="postflood_dem_05", #this is changing every pull
    evalscript=evalscriptdem,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.DEM.define_from(
                    "dem", service_url=config.sh_base_url
                ),          
            time_interval=('2017-09-20', '2017-09-28'),          
            other_args={"dataFilter": {"demInstance": "COPERNICUS_30"},"processing": {"upsampling": "NEAREST","downsampling": "NEAREST"}}
        ),
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
    ],
    bbox=bbox5,
    size=size5,
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


#old api request for comparison

# request = SentinelHubRequest(
#     data_folder="preflood_VH_05", #this is changing every pull
#     evalscript=evalscriptVH_decible,
#     input_data=[
#         SentinelHubRequest.input_data(
#             data_collection=DataCollection.SENTINEL1_IW.define_from(
#                     "s1iw", service_url=config.sh_base_url
#                 ),          
#             time_interval=('2017-09-01', '2017-09-16'), #this is chnaging depending on pre or post flood         
#             other_args={"dataFilter": {"mosaickingOrder": "mostRecent"},"processing": {"backCoeff": "GAMMA0_TERRAIN","orthorectify": True,"demInstance": "COPERNICUS","speckleFilter": {"type": "LEE","windowSizeX": 3,"windowSizeY": 3}}}
#         ),
#     ],
#     responses=[
#         SentinelHubRequest.output_response('default', MimeType.TIFF),
#     ],
#     bbox=bbox5,
#     size=size5,
#     config=config
# )

