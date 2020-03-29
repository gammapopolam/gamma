from osgeo import gdal, gdal_array
import numpy as np
import scipy

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from scipy import ndimage, misc

format = 'GTiff'
driver = gdal.GetDriverByName(format)
metadata = driver.GetMetadata()
app = QApplication([])
files, _ = QFileDialog.getOpenFileNames(None, 'Choose files', 'C:/')

print(len(files))
rasterinfo = gdal.Open(files[1])
datatype = rasterinfo.GetRasterBand(1).DataType
print(datatype)
x = rasterinfo.RasterXSize
y = rasterinfo.RasterYSize
proj = rasterinfo.GetProjection()
transform = rasterinfo.GetGeoTransform()
rasterinfo = None
print(x, y)
outputname, _ = QFileDialog.getSaveFileName(None, 'Save file')
output = driver.Create(outputname, x, y, 5, gdal.GDT_UInt16)
output.SetProjection(proj)
output.SetGeoTransform(transform)

print('1')
band1 = gdal.Open(files[2])
bandarr1 = band1.GetRasterBand(1).ReadAsArray()
blue = output.GetRasterBand(1)
blue.SetDescription('Blue band (2) Res 10m Wave 458-523')
blue.WriteArray(bandarr1)

print('2')
band2 = gdal.Open(files[3])
bandarr2 = band2.GetRasterBand(1).ReadAsArray()
green = output.GetRasterBand(2)
green.SetDescription('Green band (3) Res 10m Wave 543-578')
green.WriteArray(bandarr2)

print('3')
band3 = gdal.Open(files[4])
bandarr3 = band3.GetRasterBand(1).ReadAsArray()
red = output.GetRasterBand(3)
red.SetDescription('Red band (4) Res 10m Wave 650-680')
red.WriteArray(bandarr3)

print('4')
band4 = gdal.Open(files[5])
bandarr4 = band4.GetRasterBand(1).ReadAsArray()
VRE1 = output.GetRasterBand(4)
VRE1.SetDescription('VRE1 band (5) Res 20m Wave 698-713')
bandarr4 = ndimage.zoom(bandarr4, 2, order=1)
VRE1.WriteArray(bandarr4)

print('5')
band5 = gdal.Open(files[6])
bandarr5 = band5.GetRasterBand(1).ReadAsArray()
VRE2 = output.GetRasterBand(5)
VRE2.SetDescription('VRE2 band (6) Res 20m Wave 733-748')
bandarr5 = ndimage.zoom(bandarr5, 2, order=1)
VRE2.WriteArray(bandarr5)

output = None
print('end')
