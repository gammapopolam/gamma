# coding=utf-8

# Сделал универсальный скрипт для обработки данных Sentinel 2. Функционирует полностью, но могут быть ошибки и баги.
# Требуемые для работы модули: scipy, PyQt5, gdal.
# В будущем планирую сделать отдельным исполняемым файлом.
# by gammapopolam

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import gdal
from scipy import ndimage, misc

app = QApplication([])
QMessageBox.question(None, 'Начало работы', 'Эта программа создана для объединения каналов снимка КА Sentinel-2 MSI в '
                                            'один файл. \nБудьте внимательны: рекомендуется выбирать все каналы, включая 8А. Каналы разрешения 20м/пикс и 60м/пикс будут интерполированы к 10м/пикс.',
                     QMessageBox.Ok, QMessageBox.Ok)
inputs, _ = QFileDialog.getOpenFileNames(None, 'Choose files', 'C:/')

if not inputs:
    QMessageBox.question(None, 'Экая неудача.', "Произошла ошибка. Выберите снова файлы", QMessageBox.Ok,
                         QMessageBox.Ok)

print(inputs[1])
type_sat = 'MSI'  # sentinel 2 - фича старой версии

band = gdal.Open(inputs[0])
proj = band.GetProjection()
transform = band.GetGeoTransform()
xsize = 10980 #по умолчанию стоит разрешение 10980, это разрешение 10м/пикс, т.к. мы интерполируем к 10 метрам все 20-метровые и 60-метровые
ysize = 10980
band = None #закрываем инфоканал

format = 'GTiff'
driver = gdal.GetDriverByName(format)
metadata = driver.GetMetadata()
outputname, _ = QFileDialog.getSaveFileName(None, 'Save file')
if outputname is None:
    QMessageBox.question(None, 'Экая неудача.', "Произошла ошибка. Выберите снова файл", QMessageBox.Ok, QMessageBox.Ok)
output = driver.Create(str(outputname), xsize, ysize, 13, gdal.GDT_UInt16)

for i in range(len(inputs)):
    print('Processing ', i + 1, ' band')
    if 'B05' in inputs[i] or 'B06' in inputs[i] or 'B07' in inputs[i] or 'B8A' in inputs[i] or 'B11' in inputs[i] or 'B12' in inputs[i]: #все 20-метровые
        band = gdal.Open(str(inputs[i]))
        arr = band.GetRasterBand(1).ReadAsArray()
        arr1 = ndimage.zoom(arr, 2, order=1)
        output.GetRasterBand(i + 1).WriteArray(arr1)
        band = None
        arr = None
        arr1 = None
    elif 'B09' in inputs[i] or 'B01' in inputs[i] or 'B10' in inputs[i]: #все 60-метровые
        band = gdal.Open(str(inputs[i]))
        arr = band.GetRasterBand(1).ReadAsArray()
        arr1 = ndimage.zoom(arr, 6, order=1)
        output.GetRasterBand(i + 1).WriteArray(arr1)
        band = None
        arr = None
        arr1 = None
    else:
        band = gdal.Open(str(inputs[i]))
        arr = band.GetRasterBand(1).ReadAsArray()
        output.GetRasterBand(i + 1).WriteArray(arr)
        band = None
        arr = None
output.GetRasterBand(1).SetDescription('B1 - coastal aerosol 60m/pix')
output.GetRasterBand(2).SetDescription('B2 - blue 10m/pix')
output.GetRasterBand(3).SetDescription('B3 - green 10m/pix')
output.GetRasterBand(4).SetDescription('B4 - red 10m/pix')
output.GetRasterBand(5).SetDescription('B5 - VRE1 20m/pix')  # bilinear interpolation
output.GetRasterBand(6).SetDescription('B6 - VRE2 20m/pix')  # bilinear interpolation
output.GetRasterBand(7).SetDescription('B7 - VRE3 20m/pix')  # bilinear interpolation
output.GetRasterBand(8).SetDescription('B8 - NIR 10m/pix')
output.GetRasterBand(9).SetDescription('B8A - VRE4 20m/pix')  # bilinear interpolation
output.GetRasterBand(10).SetDescription('B9 - water vapour 60m/pix')
output.GetRasterBand(11).SetDescription('B10 - SWIR1 cirrus 60m/pix')
output.GetRasterBand(12).SetDescription('B11 - SWIR2 20m/pix')  # bilinear interpolation
output.GetRasterBand(13).SetDescription('B12 - SWIR3 20m/pix')  # bilinear interpolation
output.SetProjection(proj)
output.SetGeoTransform(transform)
output = None

QMessageBox.question(None, 'Сохранено', "Объединение завершено. Вы можете открыть файл в QGIS/ArcGIS", QMessageBox.Ok,
                     QMessageBox.Ok)
