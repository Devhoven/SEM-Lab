import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ReadImage import getImage


class ReadImageThread(QThread):

    imageLoaded = pyqtSignal(np.ndarray)
    updateInfo = pyqtSignal(str)

    def __init__(self):
        super(ReadImageThread, self).__init__()
        self.running = False

    def startGetImage(self):
        self.start()
        self.running = True

    def run(self):
        self.imageLoaded.emit(getImage(self.updateInfo))
        while self.running:
            pass

    def close(self):
        self.running = False