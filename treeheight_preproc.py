from osgeo import osr, gdal
import numpy as np
import numpy.ma as ma
import geopandas
import matplotlib.pyplot as plt

filedir = '/Users/verena/Documents/Master_ETH/masterthesis/climathon/Daten_Climathon/GEODATAS/'
ds = gdal.Open(filedir + 'LIDAR_data_laserscan_tiff/BaumhoehenAbs_LIDAR5_50cm_STZH.tif')

iextract = False #whether to read in whole data or use already processed npy dumps

if iextract:
    # extract data 
    data = ds.ReadAsArray()
    #test = data[::100,::100] #DEBUG
    test = data

    # get coordinate information
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3] 
    x = np.linspace(minx, maxx, test.shape[1])
    y = np.linspace(miny, maxy, test.shape[0])
    meshx, meshy = np.meshgrid(x,y)
    meshx[np.isnan(test)] = np.nan
    meshy[np.isnan(test)] = np.nan

    # cut out our area
    xmax = 2683893.1457
    xmin = 2683693.1448
    ymax = 1248928.9707
    ymin = 1248727.9700
    boolarr = (meshx < xmax) & (meshx > xmin) & (meshy < ymax) & (meshy > ymin)
    data_poly = test[(meshx < xmax) & (meshx > xmin) & (meshy < ymax) & (meshy > ymin)]
    x_poly = meshx[(meshx < xmax) & (meshx > xmin) & (meshy < ymax) & (meshy > ymin)]
    y_poly = meshy[(meshx < xmax) & (meshx > xmin) & (meshy < ymax) & (meshy > ymin)]
    data_poly.dump('data.npy')
    x_poly.dump('x.npy')
    y_poly.dump('y.npy')

else:
    data = np.load('data.npy')
    x = np.load('x.npy')
    y = np.load('y.npy')



# calculate LAI
def calc_LAI(treeheight):
    LAI = 0.15 * treeheight  
    return LAI

def add_tree(x0,y0,r0,h0):
    #raster = np.zeros((2000,21792))
    raster = np.zeros((400,400))
    raster[x0,y0] = h0

    for x in range(x0-r0,x0+r0):
        for y in range(y0-r0,y0+r0):
            #raster[x0-r0:x0+r0,y0-r0:y0+r0]
            raster[x,y] = np.sqrt(min(r0-x0+x, x0+r0-x)**2. + min(r0-y0+y, y0+r0-y)**2.)*h0/r0
            #np.sqrt(min(r0-x0+x, x0+r0-x)**2. + min(r0-y0+y, y0+r0-y)**2.)*h0/r0

    return raster

def calc_polygon_LAI(treeheight, area=200*200):
    LAI = calc_LAI(treeheight)
    return ma.average(LAI)

# LAI before adding tree 
LAI_before = calc_polygon_LAI(data) 

# adding 2 trees
tree1 = add_tree(250,250,10*2,30.)
tree2 = add_tree(270,270,8*2,20.)
tree1[0,0] = tree1[-1,-1] = 1.
tree2[0,0] = tree2[-1,-1] = 1.
x_norm = (x - min(x)) / (max(x) - min(x))
y_norm = (y - min(y)) / (max(y) - min(y))
x_tree1, y_tree1 = np.nonzero(tree1)
data_tree1 = tree1[x_tree1,y_tree1]
x_tree1_norm = (x_tree1 - min(x_tree1)) / (max(x_tree1) - min(x_tree1))
y_tree1_norm = (y_tree1 - min(y_tree1)) / (max(y_tree1) - min(y_tree1))
x_tree2, y_tree2 = np.nonzero(tree2)
data_tree2 = tree2[x_tree2,y_tree2]
x_tree2_norm = (x_tree2 - min(x_tree2)) / (max(x_tree2) - min(x_tree2))
y_tree2_norm = (y_tree2 - min(y_tree2)) / (max(y_tree2) - min(y_tree2))

# calculate LAI after adding trees
LAI_added = calc_polygon_LAI(tree1) + calc_polygon_LAI(tree2)
LAI_after = LAI_before + LAI_added

# plot
fontsize = 12
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
ax.set_aspect((x1-x0)/(y1-y0))
im = ax.scatter(x_norm, y_norm, c=data.flatten())
im = ax.scatter(x_tree1_norm, y_tree1_norm, c=data_tree1)
im = ax.scatter(x_tree2_norm, y_tree2_norm, c=data_tree2)
im.axes.get_xaxis().set_visible(False)
im.axes.get_yaxis().set_visible(False)
cax = fig.add_axes([0.125, 0.05, 0.77, 0.05])
cb = fig.colorbar(im, cax=cax, orientation='horizontal')
cb.ax.tick_params(labelsize=fontsize)
plt.show()
