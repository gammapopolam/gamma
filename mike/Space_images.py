class Space_images:
    def NDVI(self):
        raise NotImplementedError("Необходимо переопределить метод")

    def getBand(self, num):
        raise NotImplementedError()

    def marge(self):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()
