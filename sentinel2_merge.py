from osgeo import gdal

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

output=driver.Create('C:/KRASNOYARSK/sentinel2.tif', x, y, len(files), gdal.GDT_UInt16)
output.SetProjection(proj)
output.SetGeoTransform(transform)

for i in range (len(files)):
    print(i)
    band = gdal.Open(files[i])
    print(band.RasterXSize, band.RasterYSize)
    '''
    bandarr = band.GetRasterBand(1).ReadAsArray()
    bandarr[bandarr == 0] = np.nan
    output.GetRasterBand(i+1).WriteArray(bandarr)
    '''