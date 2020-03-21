import gdal
from setuptools import glob

from mike.Space_images import Space_images


class Landsat8(Space_images):

    def __init__(self, directory_path):
        super().__init__()
        self.bandList = []
        for path in glob.glob(directory_path + "/*.tif"):
            self.bandList.append(gdal.Open(path))

    def getBand(self, num):
        return self.bandList[num]





