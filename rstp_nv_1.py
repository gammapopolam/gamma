# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMessageBox, QRadioButton, QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QDesktopWidget, QListWidget, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
import gdal
import numpy
import numpy.ma as ma
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class RSTP(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'RSTP'
        self.left = 0
        self.top = 0
        self.width = 480
        self.height = 720
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Initialize tab screen
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setGeometry(0, 0, 1280, 720)
        self.tab1()
        self.tab2()
        # self.tab3() #inactive
        self.tab4()
        self.show()

    def tab1(self):  # объединение
        # Add tab
        self.tab1 = QWidget(self)
        self.tabwidget.addTab(self.tab1, "Merging")
        # Add objects to the tab1
        # радиокнопки
        self.landsat8 = QRadioButton('Landsat 8', self.tab1)
        self.landsat8.setGeometry(0, 0, 100, 20)
        self.landsat7 = QRadioButton('Landsat 7', self.tab1)
        self.landsat7.setGeometry(0, 20, 100, 20)
        self.landsat5 = QRadioButton('Landsat 5', self.tab1)
        self.landsat5.setGeometry(0, 40, 100, 20)
        self.sentinel2 = QRadioButton('Sentinel 2', self.tab1)
        self.sentinel2.setGeometry(0, 60, 100, 20)
        # кнопка для выбора файлов
        self.choose_input = QPushButton('Выберите файлы', self.tab1)
        self.choose_input.setGeometry(0, 100, 200, 20)
        self.choose_input.clicked.connect(self.choose_files)
        # куда выводится выбор файлов
        self.input_list = QListWidget(self.tab1)
        self.input_list.setGeometry(0, 120, 200, 400)
        # кнопка начала процесса объединения
        self.start_merging = QPushButton("Начать объединение", self.tab1)
        self.start_merging.setGeometry(0, 540, 200, 20)
        self.start_merging.clicked.connect(self.merging_process)
        # кнопка сохранения
        self.save_merging = QPushButton('Сохранить результат', self.tab1)
        self.save_merging.setGeometry(0, 560, 200, 20)
        self.save_merging.clicked.connect(self.merging_save)
        # кнопка вывода изображения в натуральных цветах
        self.rgb_btn = QPushButton("Вывод в натуральных цветах", self.tab1)
        self.rgb_btn.setGeometry(0, 580, 200, 20)
        self.rgb_btn.clicked.connect(self.rgb_show)
        self.false1_btn = QPushButton('Вывод в искусственных цветах', self.tab1)
        self.false1_btn.setGeometry(0, 600, 200, 20)
        self.false1_btn.clicked.connect(self.false1_show)
        self.water_surface_btn = QPushButton('Вывод в сочетании ИК-каналов', self.tab1)
        self.water_surface_btn.setGeometry(0, 620, 200, 20)
        self.water_surface_btn.clicked.connect(self.water_surface_show)
        # удаление данных из памяти
        self.btn_del = QPushButton('Удаление из памяти данных', self.tab1)
        self.btn_del.setGeometry(0, 640, 200, 20)
        self.btn_del.clicked.connect(self.del_processed)

    def tab2(self):  # яркостная температура
        self.tab2 = QWidget(self)

        # Add tabs
        self.tabwidget.addTab(self.tab2, "BT")
        # радиокнопки
        self.TIRS = QRadioButton('Landsat 8 TIRS', self.tab2)
        self.TIRS.setGeometry(0, 0, 120, 20)
        self.ETM = QRadioButton('Landsat 7 ETM+', self.tab2)
        self.ETM.setGeometry(0, 20, 120, 20)
        self.TM = QRadioButton('Landsat 5 TM', self.tab2)
        self.TM.setGeometry(0, 40, 120, 20)
        self.MSI = QRadioButton('Sentinel 2 MSI', self.tab2)
        self.MSI.setGeometry(0, 60, 120, 20)
        # выбор канала
        self.thermal_select = QPushButton('Выберите канал', self.tab2)
        self.thermal_select.setGeometry(0, 80, 200, 20)
        self.thermal_select.clicked.connect(self.bt_select)
        # сохранение
        self.thermal_save = QPushButton('Сохранить файл', self.tab2)
        self.thermal_save.setGeometry(0, 100, 200, 20)
        self.thermal_save.clicked.connect(self.bt_save)
        # показ
        self.thermal_show = QPushButton('Показ результата', self.tab2)
        self.thermal_show.setGeometry(0, 120, 200, 20)
        self.thermal_show.clicked.connect(self.bt_show)
        # удаление
        self.thermal_del = QPushButton('Удаление из памяти данных', self.tab2)
        self.thermal_del.setGeometry(0, 140, 200, 20)
        self.thermal_del.clicked.connect(self.bt_del)

    def tab3(self):  # вегетационный индекс, неактивно
        self.tab3 = QWidget(self)
        self.tabwidget.addTab(self.tab3, "NDVI")
        self.ndvi_select = QPushButton('Выберите каналы', self.tab3)
        self.ndvi_select.setGeometry(0, 0, 200, 20)
        self.ndvi_select.clicked.connect(self.ndvi_selection)
        self.ndvi_list = QListWidget(self.tab3)
        self.ndvi_list.setGeometry(0, 20, 200, 200)
        self.ndvi_save = QPushButton('Сохранить данные NDVI', self.tab3)
        self.ndvi_save.setGeometry(0, 220, 200, 20)
        self.ndvi_save.clicked.connect(self.ndvi_saving)
        self.ndvi_show = QPushButton('Показ данных NDVI', self.tab3)
        self.ndvi_show.setGeometry(0, 240, 200, 20)
        self.ndvi_Show.clicked.connect(self.ndvi_showing, self.tab3)

    def tab4(self):  # кластеризация
        self.tab4 = QWidget(self)
        self.tabwidget.addTab(self.tab4, 'Clustering')
        self.cluster_select = QPushButton('Выберите мульти-\nспектральный набор данных', self.tab4)
        self.cluster_select.setGeometry(0, 0, 200, 40)
        self.cluster_select.clicked.connect(self.cluster_selection)

    def choose_files(self):
        self.input_list.clear()
        self.fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', 'C:/')
        if not self.fname:
            print('Please, select files again')
        else:
            print(self.fname)
            for i in self.fname:
                self.input_list.addItem(str(i))
            for i in range(len(self.fname)):
                print(self.fname[i])

    def merging_process(self):
        self.bands = 0
        print('проверка условия')
        if self.sentinel2.isChecked():
            band = gdal.Open(str(self.fname[2]))
            self.x = band.RasterXSize
            self.y = band.RasterYSize
            self.proj = band.GetProjection()
            self.transform = band.GetGeoTransform()
            band = None
            print('условие пройдено')
            print(self.x, self.y)
        else:
            band = gdal.Open(str(self.fname[1]))
            self.x = band.RasterXSize
            self.y = band.RasterYSize
            self.proj = band.GetProjection()
            self.transform = band.GetGeoTransform()
            band = None
            print('условие пройдено')
            print(self.x, self.y)
        print('пробегаемся по каналам')
        for i in range(len(self.fname)):
            self.bands = self.bands + 1
            print(self.bands)
            band = gdal.Open(str(self.fname[i]))
            print('большое условие')
            if self.landsat8.isChecked():  # ландсат 8
                # к нормализованным добавить множитель uint16bit, выводить через matplotlib нормализованные, а в файл добавлять ненормализованные
                if 'B1' in self.fname[i]:
                    self.coastal_aerosol = band.GetRasterBand(1).ReadAsArray()
                    self.coastal_aerosol[self.coastal_aerosol == 0] = numpy.nan
                elif 'B2' in self.fname[i]:
                    self.blue = band.GetRasterBand(1).ReadAsArray()
                    self.blue[self.blue == 0] = numpy.nan
                elif 'B3' in self.fname[i]:
                    self.green = band.GetRasterBand(1).ReadAsArray()
                    self.green[self.green == 0] = numpy.nan
                elif 'B4' in self.fname[i]:
                    self.red = band.GetRasterBand(1).ReadAsArray()
                    self.red[self.red == 0] = numpy.nan
                elif 'B5' in self.fname[i]:
                    self.NIR = band.GetRasterBand(1).ReadAsArray()
                    self.NIR[self.NIR == 0] = numpy.nan
                elif 'B6' in self.fname[i]:
                    self.SWIR1 = band.GetRasterBand(1).ReadAsArray()
                    self.SWIR1[self.SWIR1 == 0] = numpy.nan
                elif 'B7' in self.fname[i]:
                    self.SWIR2 = band.GetRasterBand(1).ReadAsArray()
                    self.SWIR2[self.SWIR2 == 0] = numpy.nan
            elif self.landsat7.isChecked() or self.landsat5.isChecked():  # ландсат 7, 5
                if 'B1' in self.fname[i]:
                    self.blue = band.GetRasterBand(1).ReadAsArray()
                    self.blue[self.blue == 0] = numpy.nan
                elif 'B2' in self.fname[i]:
                    self.green = band.GetRasterBand(1).ReadAsArray()
                    self.green[self.green == 0] = numpy.nan
                elif 'B3' in self.fname[i]:
                    self.red = band.GetRasterBand(1).ReadAsArray()
                    self.red[self.red == 0] = numpy.nan
                elif 'B4' in self.fname[i]:
                    self.NIR = band.GetRasterBand(1).ReadAsArray()
                    self.NIR[self.NIR == 0] = numpy.nan
                elif 'B5' in self.fname[i]:
                    self.SWIR1 = band.GetRasterBand(1).ReadAsArray()
                    self.SWIR1[self.SWIR1 == 0] = numpy.nan
                elif 'B6' in self.fname[i]:
                    self.TIR = band.GetRasterBand(1).ReadAsArray()
                    self.TIR[self.TIR == 0] = numpy.nan
                elif 'B7' in self.fname[i]:
                    self.SWIR2 = band.GetRasterBand(1).ReadAsArray()
                    self.SWIR2[self.SWIR2 == 0] = numpy.nan
            elif self.sentinel2.isChecked():  # сентинель 2
                if 'B01' in self.fname[i]:
                    self.coastal_aerosol = band.GetRasterBand(1).ReadAsArray()
                elif 'B02' in self.fname[i]:
                    self.blue = band.GetRasterBand(1).ReadAsArray()
                    #self.blue[self.blue == 0] = numpy.nan
                elif 'B03' in self.fname[i]:
                    self.green = band.GetRasterBand(1).ReadAsArray()
                    #self.green[self.green == 0] = numpy.nan
                elif 'B04' in self.fname[i]:
                    self.red = band.GetRasterBand(1).ReadAsArray()
                    #self.red[self.red == 0] = numpy.nan
                elif 'B05' in self.fname[i]:
                    self.VRE1 = band.GetRasterBand(1).ReadAsArray()
                    #self.VRE1[self.VRE1 == 0] = numpy.nan
                elif 'B06' in self.fname[i]:
                    self.VRE2 = band.GetRasterBand(1).ReadAsArray()
                    #self.VRE2[self.green == 0] = numpy.nan
                elif 'B07' in self.fname[i]:
                    self.VRE3 = band.GetRasterBand(1).ReadAsArray()
                    #self.VRE3[self.VRE3 == 0] = numpy.nan
                elif 'B08' in self.fname[i]:
                    self.NIR = band.GetRasterBand(1).ReadAsArray()
                    #self.NIR[self.NIR == 0] = numpy.nan
                elif 'B09' in self.fname[i]:
                    self.water_vapour = band.GetRasterBand(1).ReadAsArray()
                    #self.water_vapour[self.water_vapour == 0] = numpy.nan
                elif 'B10' in self.fname[i]:
                    self.SWIR1 = band.GetRasterBand(1).ReadAsArray()
                    #self.SWIR1[self.SWIR1 == 0] = numpy.nan
                elif 'B11' in self.fname[i]:
                    self.SWIR2 = band.GetRasterBand(1).ReadAsArray()
                    #self.SWIR2[self.SWIR2 == 0] = numpy.nan
                elif 'B12' in self.fname[i]:
                    self.SWIR3 = band.GetRasterBand(1).ReadAsArray()
                    #self.SWIR3[self.SWIR3 == 0] = numpy.nan

        QMessageBox.question(self, 'Предпроцесс завершён', 'Начните сохранение обработанных данных или их показ',
                             QMessageBox.Ok, QMessageBox.Ok)

    def merging_save(self):
        print('start stacking')
        format = "GTiff"
        driver = gdal.GetDriverByName(format)
        metadata = driver.GetMetadata()
        outputname, _ = QFileDialog.getSaveFileName(self, 'Save file')
        if outputname is None:
            QMessageBox.question(self, 'Выберите снова', "ВЫберите снова файл", QMessageBox.Ok, QMessageBox.Ok)
        output = driver.Create(str(outputname), self.x, self.y, self.bands, gdal.GDT_UInt16)
        if self.landsat8.isChecked():
            format = "GTiff"
            allbands = numpy.stack((self.coastal_aerosol, self.blue, self.green, self.red, self.NIR, self.SWIR1, self.SWIR2))
            for i in range(self.bands):
                output.GetRasterBand(i + 1).WriteArray(allbands[i])
        elif self.landsat7.isChecked() or self.landsat5.isChecked():
            allbands = numpy.stack((self.blue, self.green, self.red, self.NIR, self.SWIR1, self.TIR, self.SWIR2))
            for i in range(self.bands):
                output.GetRasterBand(i + 1).WriteArray(allbands[i])
        elif self.sentinel2.isChecked():
            for i in range(self.bands):
                print('большое сохранение')
                if i + 1 == 1:
                    output.GetRasterBand(i + 1).WriteArray(self.coastal_aerosol)
                elif i + 1 == 2:
                    output.GetRasterBand(i + 1).WriteArray(self.blue)
                elif i + 1 == 3:
                    output.GetRasterBand(i + 1).WriteArray(self.green)
                elif i + 1 == 4:
                    output.GetRasterBand(i + 1).WriteArray(self.red)
                elif i + 1 == 5:
                    output.GetRasterBand(i + 1).WriteArray(self.VRE1)
                elif i + 1 == 6:
                    output.GetRasterBand(i + 1).WriteArray(self.VRE2)
                elif i + 1 == 7:
                    output.GetRasterBand(i + 1).WriteArray(self.VRE3)
                elif i + 1 == 8:
                    output.GetRasterBand(i + 1).WriteArray(self.NIR)
                elif i + 1 == 9:
                    output.GetRasterBand(i + 1).WriteArray(self.water_vapour)
                elif i + 1 == 10:
                    output.GetRasterBand(i + 1).WriteArray(self.SWIR1)
                elif i + 1 == 11:
                    output.GetRasterBand(i + 1).WriteArray(self.SWIR2)
                elif i + 1 == 12:
                    output.GetRasterBand(i + 1).WriteArray(self.SWIR3)
        output.SetProjection(self.proj)
        output.SetGeoTransform(self.transform)
        allbands = None
        output = None

        QMessageBox.question(self, 'Сохранение завершено', 'Теперь вы можете открыть сохраненный файл в QGIS/ArcGIS',
                             QMessageBox.Ok, QMessageBox.Ok)
    def rgb_show(self):  # натуральные цвета
        if self.landsat8.isChecked():
            rgb = numpy.dstack((self.red, self.green, self.blue))
            scaled_rgb = (rgb * (255 / 65535)).astype(numpy.uint8)

            plotted = plt.imshow(scaled_rgb)
            plt.xlabel('Сочетание красного, зелёного и синего каналов')
            plt.show()
        if self.landsat7.isChecked() or self.landsat5.isChecked():
            rgb = numpy.dstack((self.red, self.green, self.blue))
            plotted = plt.imshow(rgb)
            plt.xlabel('Сочетание красного, зелёного и синего каналов')
            plt.show()
        if self.sentinel2.isChecked():
            QMessageBox.question(self, 'Недоступно', "К сожалению, показ недоступен для Sentinel 2", QMessageBox.Ok, QMessageBox.Ok)
            '''
            rgb = numpy.dstack((self.red, self.green, self.blue))
            scaled_rgb = (rgb * (255 / 65535)).astype(numpy.uint8)

            plotted = plt.imshow(rgb)
            plt.xlabel('Сочетание красного, зелёного и синего каналов')
            plt.show()
            '''
    def false1_show(self):  # инфракрасный, ближний ИК + красный + зеленый
        if self.landsat8.isChecked():
            nrg = numpy.dstack((self.NIR, self.red, self.green))
            scaled_nrg = (nrg * (255 / 65535)).astype(numpy.uint8)

            plotted = plt.imshow(scaled_nrg)
            plt.xlabel('Сочетание красного, зелёного и синего каналов')
            plt.show()
        if self.landsat7.isChecked() or self.landsat5.isChecked():
            nrg = numpy.dstack((self.NIR, self.red, self.green))
            plotted = plt.imshow(nrg)
            plt.xlabel('Сочетание красного, зелёного и синего каналов')
            plt.show()
        if self.sentinel2.isChecked():
            QMessageBox.question(self, 'Недоступно', "К сожалению, показ недоступен для Sentinel 2", QMessageBox.Ok, QMessageBox.Ok)
    def water_surface_show(self):  # проникает через дым, SWIR2+SWIR1+NIR
        if self.landsat8.isChecked():
            water_surface = numpy.dstack((self.SWIR2, self.SWIR1, self.NIR))
            scaled_water_surface = (water_surface * (255 / 65535)).astype(numpy.uint8)
            plotted = plt.imshow(scaled_water_surface)
            plt.xlabel('Сочетание ИК каналов')
            plt.show()
        if self.landsat7.isChecked() or landsat5.isChecked():
            water_surface = numpy.dstack((self.SWIR2, self.SWIR1, self.NIR))
            plotted = plt.imshow(water_surface)
            plt.xlabel('Сочетание ИК каналов')
            plt.show()
        if self.sentinel2.isChecked():
            QMessageBox.question(self, 'Недоступно', "К сожалению, показ недоступен для Sentinel 2", QMessageBox.Ok, QMessageBox.Ok)

    def del_processed(self):
        del self.coastal_aerosol, self.blue, self.green, self.red, self.NIR, self.SWIR1, self.SWIR2, self.SWIR3, self.VRE1, self.VRE2, self.VRE3, self.TIR
        self.input_list.clear()
        del self.x, self.y, self.proj, self.transform
        self.bands=0
        self.fname = []
        QMessageBox.question(self, '[ДАННЫЕ УДАЛЕНЫ]', 'Данные удалены из памяти', QMessageBox.Ok, QMessageBox.Ok)


    def bt_select(self):
        # считывание метадаты
        metaname, _ = QFileDialog.getOpenFileName(self, 'Open metadata', 'C:/',
                                                  'Text files (*.txt);;Текстовый документ (*.txt)')
        if not metaname:
            print('Please, select file again')
        else:
            print(metaname)
        # считывание канала
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:/',
                                               'TIF format (*.tif *.TIF);;TIFF format (*.tiff *.TIFF)')
        if fname == '':
            print('Please, select file again')
        else:
            thermalds = gdal.Open(fname)
            thermalband = thermalds.GetRasterBand(1)
            print(fname)
            self.x = thermalds.RasterXSize
            self.y = thermalds.RasterYSize
            self.proj = thermalds.GetProjection()
            self.transform = thermalds.GetGeoTransform()

        if self.TIRS.isChecked():
            # проверка констант через mtl файл
            if 'B10' in fname:
                metadata = open(metaname)
                for line in metadata:
                    if 'K1_CONSTANT_BAND_10' in line:
                        K1_CONSTANT_BAND_10 = float(line[26:-2])
                        print(K1_CONSTANT_BAND_10)
                    elif 'K2_CONSTANT_BAND_10' in line:
                        K2_CONSTANT_BAND_10 = float(line[26:-2])
                        print(K2_CONSTANT_BAND_10)
                therm1 = numpy.array(thermalband.ReadAsArray(), dtype=numpy.float32)
                therm1[therm1 == 0] = numpy.nan

                therm_radiance = (therm1 * 0.0003342) + 0.1

                self.therm_BT = K2_CONSTANT_BAND_10 / numpy.log((K1_CONSTANT_BAND_10 / therm_radiance) + 1)
            elif 'B11' in fname:
                metadata = open(metaname)
                for line in metadata:
                    if 'K1_CONSTANT_BAND_11' in line:
                        K1_CONSTANT_BAND_11 = float(line[26:-2])
                        print(K1_CONSTANT_BAND_11)
                    elif 'K2_CONSTANT_BAND_11' in line:
                        K2_CONSTANT_BAND_11 = float(line[26:-2])
                        print(K2_CONSTANT_BAND_11)
                therm1 = numpy.array(thermalband.ReadAsArray(), dtype=numpy.float32)
                therm1[therm1 == 0] = numpy.nan

                therm_radiance = (therm1 * 0.0003342) + 0.1
                self.therm_BT = K2_CONSTANT_BAND_11 / numpy.log((K1_CONSTANT_BAND_11 / therm_radiance) + 1)
        QMessageBox.question(self, 'Предпроцесс завершен',
                             'Вы можете сохранить файл с результатом или отобразить его в отдельном окне',
                             QMessageBox.Ok, QMessageBox.Ok)

    def bt_save(self):
        format = "GTiff"
        driver = gdal.GetDriverByName(format)
        metadata = driver.GetMetadata()
        outputname, _ = QFileDialog.getSaveFileName(self, 'Save file', 'C:/')
        output = driver.Create(str(outputname), self.x, self.y, 1, gdal.GDT_Float32)
        output.GetRasterBand(1).WriteArray(self.therm_BT)
        output.SetProjection(self.proj)
        output.SetGeoTransform(self.transform)
        output = None
        QMessageBox.question(self, 'Файл сохранен', 'Файл сохранен успешно', QMessageBox.Ok, QMessageBox.Ok)

    def bt_show(self):  # показ яркостной температуры
        plotted = plt.imshow(self.therm_BT)
        plt.xlabel('Brightness temperature, Celsius')
        plt.show()

    def bt_del(self):  # удаление из памяти данных
        del self.therm_BT

    def ndvi_selection(self):  # нужно доделать или исключить из списка инструментов
        self.ndvi_list.clear()
        fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', 'C:/')
        if fname == [] or len(fname) > 2:
            print('Please, select files again or select only two channels')
            QMessageBox.question(self, 'Не удалось выбрать файлы',
                                 'Убедитесь, что вы выбрали красный и ближний инфракрасный каналы.', QMessageBox.Ok,
                                 QMessageBox.Ok)
        else:
            print(fname)
            for i in fname:
                self.input_list.addItem(str(i))
            for i in range(len(fname)):
                print(fname[i])
        Red = gdal.Open(fname[0])
        x = Red.RasterXSize
        y = Red.RasterYSize
        proj = Red.GetProjection()
        transform = Red.GetGeoTransform()
        NIR = gdal.Open(fname[1])
        NIRar = NIR.GetRasterBand(1).ReadAsArray().astype(numpy.float32)
        NIRarmin = NIRar.min()
        NIRarmax = NIRar.max()
        # therm_radiance=(therm1 * 0.0003342) + 0.1
        Redar = Red.GetRasterBand(1).ReadAsArray().astype(numpy.float32)
        Redarmax = Redar.max()
        Redarmin = Redar.min()
        NIRnorm = numpy.divide((NIRar - NIRarmin), (NIRarmax - NIRarmin))
        Rednorm = numpy.divide((Redar - Redarmin), (Redarmax - Redarmin))

        NDVInorm = numpy.divide((NIRnorm - Rednorm), (NIRnorm + Rednorm))
        plotted = plt.imshow(NDVInorm)
        plt.xlabel('NDVI normalized')
        plt.show()

        NDVI = numpy.divide((NIRar - Redar), (NIRar + Redar))
        plotted = plt.imshow(NDVI)
        plt.xlabel('NDVI non-normalized')
        plt.show()

        QMessageBox.question(self, 'Файл сохранен', 'Файл сохранен успешно', QMessageBox.Ok, QMessageBox.Ok)

    def ndvi_saving(self):
        a = 1
        '''
        format = "GTiff"
        driver = gdal.GetDriverByName( format )
        metadata = driver.GetMetadata()
        outputname, _ = QFileDialog.getSaveFileName(self, 'Save file', 'C:/')
        output=driver.Create(str(outputname), x, y, 1,  gdal.GDT_Float32)
        output.GetRasterBand(1).WriteArray(NDVI)
        output.SetProjection( proj )
        output.SetGeoTransform( transform )
        output = None
        '''

    def cluster_selection(self):
        a = 1

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RSTP()
    sys.exit(app.exec_())
