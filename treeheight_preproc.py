from osgeo import osr, gdal
import geopandas
import matplotlib.pyplot as plt

filedir = '/Users/verena/Documents/Master_ETH/masterthesis/climathon/Daten_Climathon/GEODATAS/'
treeheight = gdal.Open(filedir + 'LIDAR_data_laserscan_tiff/BaumhoehenAbs_LIDAR5_50cm_STZH.tif')
treecount = geopandas.read_file('Baumkataster_Zuerich/Baumkataster.shp')

# transform to WGS84
#old_cs= osr.SpatialReference()
#old_cs.ImportFromWkt(ds.GetProjectionRef())
#wgs84_wkt = """
#GEOGCS["WGS 84",
#    DATUM["WGS_1984",
#        SPHEROID["WGS 84",6378137,298.257223563,
#            AUTHORITY["EPSG","7030"]],
#        AUTHORITY["EPSG","6326"]],
#    PRIMEM["Greenwich",0,
#        AUTHORITY["EPSG","8901"]],
#    UNIT["degree",0.01745329251994328,
#        AUTHORITY["EPSG","9122"]],
#    AUTHORITY["EPSG","4326"]]"""
#new_cs = osr.SpatialReference()
#new_cs .ImportFromWkt(wgs84_wkt)
#transform = osr.CoordinateTransformation(old_cs,new_cs) 
#
#width = ds.RasterXSize
#height = ds.RasterYSize
#gt = ds.GetGeoTransform()
#minx = gt[0]
#miny = gt[3] + width*gt[4] + height*gt[5] 
#
#latlong = transform.TransformPoint(x,y)
#
#
width = ds.RasterXSize
height = ds.RasterYSize
gt = ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5] 
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3] 
x = np.linspace(minx, maxx, test.shape[0])
y = np.linspace(miny, maxy, test.shape[1])
meshx, meshy = np.meshgrid(y,x)
meshx[np.isnan(test)] = np.nan
meshy[np.isnan(test)] = np.nan

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
ax.scatter(meshx.flatten(), meshy.flatten(), c=test.flatten())
treecount.plot()
plt.show()

# test plot
data = treeheight.ReadAsArray()
test = data[::100,::100]
import matplotlib.pyplot as plt
plt.pcolormesh(test)
plt.show()
