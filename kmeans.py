# coding=utf-8
import numpy as np
from sklearn import cluster
from osgeo import gdal, gdal_array
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

# Tell GDAL to throw Python exceptions, and register all drivers
gdal.UseExceptions()
gdal.AllRegister()
app = QApplication([])
QMessageBox.question(None, 'Начало работы', 'Эта программа создана для классификации спутникового изображения Landsat или Sentinel-2. '
                                            '\nРекомендуется использовать многоканальный набор данных (больше 3-х каналов). \nПосле этого сообщения, введите в консоли количество классов.'
                                            '\nФайл сохранится в ту же папку, но с постфиксом _km.tif.',
                     QMessageBox.Ok, QMessageBox.Ok)
inputs, _ = QFileDialog.getOpenFileNames(None, 'Choose files', 'C:/')
print(inputs)
if not inputs:
    QMessageBox.question(None, 'Экая неудача.', "Произошла ошибка. Выберите снова файлы", QMessageBox.Ok,
                         QMessageBox.Ok)
print('Введите количество классов:')
n_clusters=int(input())
string=''.join(inputs) 
print(string)
outputs=string[:-4]+'_km.tif'
print('opening')
img_ds = gdal.Open(string, gdal.GA_ReadOnly)
band = img_ds.GetRasterBand(2)
arr = band.ReadAsArray()
[cols, rows] = arr.shape

format = "GTiff"
driver = gdal.GetDriverByName(format)

print('creating output file')
outDataRaster = driver.Create(outputs, rows, cols, 1, gdal.GDT_Byte)
outDataRaster.SetGeoTransform(img_ds.GetGeoTransform()) #sets same geotransform as input
outDataRaster.SetProjection(img_ds.GetProjection()) #sets same projection as input


img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
               gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
print('MiniBatch KMeans')
for b in range(img.shape[2]):
    img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()
new_shape = (img.shape[0] * img.shape[1], img.shape[2])
X = img[:, :, :13].reshape(new_shape)
MB_KMeans = cluster.MiniBatchKMeans(n_clusters)
MB_KMeans.fit(X)
X_cluster = MB_KMeans.labels_
X_cluster = X_cluster.reshape(img[:, :, 0].shape)
outDataRaster.GetRasterBand(1).WriteArray(X_cluster)

outDataRaster.FlushCache() ## remove from memory
del outDataRaster ## delete the data (not the actual geotiff)
QMessageBox.question(None, 'Сохранено', "Кластеризация завершена. Вы можете открыть файл в QGIS/ArcGIS", QMessageBox.Ok,
                     QMessageBox.Ok)
