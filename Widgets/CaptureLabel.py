import os
from main import *
import numpy as np
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt


class CaptureLabel(QLabel):

    clicked = pyqtSignal(QLabel)

    def __init__(self, parent):
        super(CaptureLabel, self).__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.image = None
        self.filePath = None

        self.spotSizeVal = None
        self.coarseVal = None
        self.currentVal = None
        self.voltageVal = None
        self.focusVal = None

    def setImage(self, filePath, img, width):
        self.filePath = filePath
        self.setToolTip(os.path.basename(filePath))

        self.image = np.array(img)
        qix = ImageQt(img)
        self.setPixmap(QPixmap.fromImage(qix).scaled(width, width, Qt.KeepAspectRatio))

        self.spotSizeVal = img.info['SpotSize']
        self.coarseVal = img.info['Coarse']
        self.currentVal = img.info['Current']
        self.voltageVal = img.info['Voltage']
        self.focusVal = img.info['Focus']


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        action = menu.addAction(translate("DeleteImg"))
        action.triggered.connect(lambda: self.delete())

        menu.exec_(event.globalPos())

    def delete(self):
        self.hide()
        os.remove(self.filePath)

