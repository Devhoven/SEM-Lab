import cv2
from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LUTList(QComboBox):

    def __init__(self, lutItems):
        super().__init__()

        for item in lutItems:
            self.addItem(item.icon, item.name)

        self.setIconSize(QSize(256, 30))

class LUTItem():

    def __init__(self, name, cvType):
        super().__init__()

        self.name = name
        self.cvType = cvType
        self.icon = QIcon("assets/LUTScales/colorscale_" + name.lower() + ".jpg")
