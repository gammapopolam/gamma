# coding=utf-8

# Сделал универсальный скрипт для обработки данных Landsat 5,7,8. Функционирует полностью, но могут быть ошибки и баги.
# Требуемые для работы модули: scipy, PyQt5, gdal.
# В будущем планирую сделать отдельным исполняемым файлом.
# by gammapopolam

import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import gdal
from scipy import ndimage

app = QApplication([])
QMessageBox.question(None, 'Начало работы', 'Эта программа создана для объединения каналов снимков КА Landsat TM/ETM+/OLI. Выбирайте каналы по порядку с 1 по 7, не включая панхроматический')
inputs, _ = QFileDialog.getOpenFileNames(None, 'Выберите файлы', 'C:/')
print(inputs[1])

if 'LC08' in inputs[0]:
    #  landsat 8
    type_sat = 'OLI'
elif 'LE07' in inputs[0]:
    #  landsat 7
    type_sat = 'ETM+'
elif 'LT05' in inputs[0]:
    #  landsat 5
    type_sat = 'TM'
elif '.jp2' in inputs[0]:
    #  sentinel 2
    type_sat = 'MSI'
    QMessageBox.question(None, 'Экая неудача.', "Похоже, что вы выбрали снимки Sentinel-2 MSI. Перезапустите приложение.", QMessageBox.Ok,
                         QMessageBox.Ok)

band = gdal.Open(inputs[0]) #инфоканал
proj = band.GetProjection()
transform = band.GetGeoTransform()
xsize = band.RasterXSize
ysize = band.RasterYSize
band = None
band1 = None

format = 'GTiff'
driver = gdal.GetDriverByName(format)
metadata = driver.GetMetadata()
outputname, _ = QFileDialog.getSaveFileName(None, 'Save file')
if outputname is None:
    QMessageBox.question(None, 'Экая неудача.', "Произошла ошибка. Выберите снова файл", QMessageBox.Ok, QMessageBox.Ok)
output = driver.Create(str(outputname), xsize, ysize, len(inputs), gdal.GDT_UInt16)
if type_sat == 'OLI':
    for i in range(len(inputs)):
        band = gdal.Open(str(inputs[i]))
        arr = band.GetRasterBand(1).ReadAsArray()
        output.GetRasterBand(i+1).WriteArray(arr)
        band = None
    #инфо для каналов
    output.GetRasterBand(1).SetDescription('B1 - coastal aerosol 30m/pix')
    output.GetRasterBand(2).SetDescription('B2 - blue 30m/pix')
    output.GetRasterBand(3).SetDescription('B3 - green 30m/pix')
    output.GetRasterBand(4).SetDescription('B4 - red 30m/pix')
    output.GetRasterBand(5).SetDescription('B5 - NIR 30m/pix')
    output.GetRasterBand(6).SetDescription('B6 - SWIR1 30m/pix')
    output.GetRasterBand(7).SetDescription('B7 - SWIR2 30m/pix')
    output.SetProjection(proj)
    output.SetGeoTransform(transform)

elif type_sat == 'ETM+' or type_sat == 'TM':
    for i in range(len(inputs)):
        if 'B6' in inputs[i]:
            band = gdal.Open(str(inputs[i]))
            arr = band.GetRasterBand(1).ReadAsArray()
            #bilinear interpolation
            arr1 = ndimage.zoom(arr, 2, order=1)
            output.GetRasterBand(i+1).WriteArray(arr1)
            band = None
            arr = None
            arr1 = None
        else:
            band = gdal.Open(str(inputs[i]))
            arr = band.GetRasterBand(1).ReadAsArray()
            output.GetRasterBand(i + 1).WriteArray(arr)
            band = None
            arr = None
    #инфо для каналов
    output.GetRasterBand(1).SetDescription('B1 - blue 30m/pix')
    output.GetRasterBand(2).SetDescription('B2 - green 30m/pix')
    output.GetRasterBand(3).SetDescription('B3 - red 30m/pix')
    output.GetRasterBand(4).SetDescription('B4 - NIR 30m/pix')
    output.GetRasterBand(5).SetDescription('B5 - SWIR1 30m/pix')
    output.GetRasterBand(6).SetDescription('B6 - TIR 60m/pix')
    #  bilinear interpolation for band6
    output.GetRasterBand(7).SetDescription('B7 - SWIR2 30m/pix')
    output.SetProjection(proj)
    output.SetGeoTransform(transform)
output = None
QMessageBox.question(None, 'Сохранено', "Объединение завершено. Вы можете открыть файл в QGIS/ArcGIS", QMessageBox.Ok,
                     QMessageBox.Ok)
