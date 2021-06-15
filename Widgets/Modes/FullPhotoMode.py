from main import *
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt
from Widgets.ImageViewer import *

class FullPhotoMode(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QHBoxLayout()

        self.setContentsMargins(20, 20, 20, 20)
        self.setMinimumSize(200, 200)

        self.imageCon = ImageViewer(self)
        self.imageCon.setMinimumSize(2000, 2000)
        layout.addWidget(self.imageCon)

        self.setLayout(layout)

    # This function accepts a numpy image and converts it into a PIL Image
    def setImageNP(self, newImage):
        # Could happen if the user starts the full photo mode before selecting an image
        if newImage is None:
            return
        im = Image.fromarray(newImage)
        im = im.convert("RGB")
        self.setImagePIL(im)

    def setImagePIL(self, newImage):
        qix = ImageQt(newImage)
        pixmap = QPixmap.fromImage(qix)
        self.imageCon.updateImage(pixmap.scaled(2050, 2050, Qt.KeepAspectRatio))
