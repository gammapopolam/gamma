from osgeo import gdal
from scipy import ndimage

format = 'GTiff'
driver = gdal.GetDriverByName(format)
metadata = driver.GetMetadata()

files = ['C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B01.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B02.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B03.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B04.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B05.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B06.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B07.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B08.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B09.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B10.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B11.jp2',
         'C:/KRASNOYARSK/L1C_T46VDH_A007724_20180829T050013/S2B_MSIL1C_20180829T045649_N0206_R119_T46VDH_20180829T103944.SAFE/GRANULE/L1C_T46VDH_A007724_20180829T050013/IMG_DATA/T46VDH_20180829T045649_B12.jp2']
print(len(files))
rasterinfo=gdal.Open(files[1])
datatype=rasterinfo.GetRasterBand(1).DataType
print(datatype)
x = rasterinfo.RasterXSize
y = rasterinfo.RasterYSize
proj = rasterinfo.GetProjection()
transform = rasterinfo.GetGeoTransform()
rasterinfo = None
print(x,y)
output=driver.Create('C:/KRASNOYARSK/sentinel2.tif', x, y, 9, gdal.GDT_UInt16)
output.SetProjection(proj)
output.SetGeoTransform(transform)

print('1')
band1=gdal.Open(files[1])
bandarr1 = band1.GetRasterBand(1).ReadAsArray()
blue = output.GetRasterBand(1)
blue.SetDescription('Blue band (2) Res 10m Wave 458-523')
blue.WriteArray(bandarr1)
bandarr1=None
print('2')
band2=gdal.Open(files[2])
bandarr2 = band2.GetRasterBand(1).ReadAsArray()
green = output.GetRasterBand(2)
green.SetDescription('Green band (3) Res 10m Wave 543-578')
green.WriteArray(bandarr2)
bandarr2=None
print('3')
band3=gdal.Open(files[3])
bandarr3 = band3.GetRasterBand(1).ReadAsArray()
red = output.GetRasterBand(3)
red.SetDescription('Red band (4) Res 10m Wave 650-680')
red.WriteArray(bandarr3)
bandarr3=None
print('4')
band4=gdal.Open(files[4])
bandarr4 = band4.GetRasterBand(1).ReadAsArray()
VRE1 = output.GetRasterBand(4)
VRE1.SetDescription('VRE1 band (5) Res 20m Wave 698-713')
bandarr4_scaled= ndimage.zoom(bandarr4, 2, order=1)
VRE1.WriteArray(bandarr4_scaled)
bandarr4 = None
bandarr4_scaled = None

print('5')
band5=gdal.Open(files[5])
bandarr5 = band5.GetRasterBand(1).ReadAsArray()
VRE2 = output.GetRasterBand(5)
VRE2.SetDescription('VRE2 band (6) Res 20m Wave 733-748')
bandarr5_scaled= ndimage.zoom(bandarr5, 2, order=1)
VRE2.WriteArray(bandarr5_scaled)
bandarr5 = None
bandarr5_scaled = None

print('6')
band6=gdal.Open(files[6])
bandarr6 = band6.GetRasterBand(1).ReadAsArray()
VRE3 = output.GetRasterBand(6)
VRE3.SetDescription('VRE3 band (7) Res 20m Wave 773-793')
bandarr6_scaled= ndimage.zoom(bandarr6, 2, order=1)
VRE3.WriteArray(bandarr6_scaled)
bandarr6 = None
bandarr6_scaled = None

print('7')
band7=gdal.Open(files[7])
bandarr7 = band7.GetRasterBand(1).ReadAsArray()
NIR = output.GetRasterBand(7)
NIR.SetDescription('NIR band (8) Res 10m Wave 785-899')
NIR.WriteArray(bandarr7)
bandarr7 = None

print('8')
band8=gdal.Open(files[4])
bandarr8 = band8.GetRasterBand(1).ReadAsArray()
SWIR1 = output.GetRasterBand(8)
SWIR1.SetDescription('SWIR1 band (11) Res 20m Wave 1565-1655')
bandarr8_scaled= ndimage.zoom(bandarr8, 2, order=1)
SWIR1.WriteArray(bandarr8_scaled)
bandarr8 = None
bandarr8_scaled = None
print('9')
band9=gdal.Open(files[4])
bandarr9 = band9.GetRasterBand(1).ReadAsArray()
SWIR2 = output.GetRasterBand(9)
SWIR2.SetDescription('SWIR2 band (12) Res 20m Wave 2100-2280')
bandarr9_scaled= ndimage.zoom(bandarr9, 2, order=1)
SWIR2.WriteArray(bandarr9_scaled)
bandarr9 = None
bandarr9_scaled = None

output = None
print('end')