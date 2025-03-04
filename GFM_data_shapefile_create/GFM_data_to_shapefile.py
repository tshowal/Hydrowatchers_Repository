import rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import shape, Polygon
import numpy as np
from rasterio.features import shapes

# File path
flood_extent_file = "GFM_data_shapefile_create/central_PR_flood_extent.tif"

# Open the raster file
with rasterio.open(flood_extent_file) as src:
    flood_array = src.read(1)  # Read first band (contains flood extent)
    transform = src.transform  # Get transform info
    crs = src.crs  # Get coordinate reference system of the raster

# Mask out NoData values (assuming 255 is NoData)
flood_array = np.where(flood_array == 255, 0, flood_array)

# Extract polygons where flood value is 1
flood_polygons = [
    (shape(geom), value) for geom, value in shapes(flood_array, transform=transform)
    if value == 1  # Keep only flooded areas
]

# Convert to a GeoDataFrame
gdf = gpd.GeoDataFrame(
    {"geometry": [poly[0] for poly in flood_polygons], "flood_value": [poly[1] for poly in flood_polygons]},
    crs=crs  # Maintain original CRS
)

# Ensure CRS is EPSG:4326 (WGS 84)
if gdf.crs is not None and gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs(epsg=4326)

# Save to a Shapefile
shapefile_path = "flood_polygons.shp"
gdf.to_file(shapefile_path, driver="ESRI Shapefile")

print(f"Flood polygons saved to {shapefile_path}")

### VIEW THE POLYGONS
# Load the shapefile
shapefile_path = "GFM_data_shapefile_create/central_PR_flood_polygons.shp"
gdf = gpd.read_file(shapefile_path)

# Plot the polygons
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color="blue", edgecolor="black", alpha=0.5)

# Add title and labels
ax.set_title("Flood Extent Polygons")
plt.show()
