import os
import glob
from main import *
from Threads.Thread import *
from PyQt5.QtWidgets import *
from Widgets.CaptureLabel import *
from Widgets.Modes.LiveMode import LiveMode
from Widgets.Modes.PhotoMode import PhotoMode
from PIL.PngImagePlugin import PngImageFile, PngInfo


class UiContainer(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)

        self.settings = settings

        # Gets the path which was saved by the user, or the path to the desktop
        self.path = self.settings.value("path", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "/")

        # Hold the threads that is used by the stream widgets
        # Saves here, so multiple stream widgets can use it
        self.liveFeedThread = None
        self.camThread = None
        self.initThreads()

        self.modeCon = QStackedWidget(self)
        self.liveMode = LiveMode(self)
        self.photoMode = PhotoMode(self)

        self.liveFeedThread.start()
        self.camThread.start()

        self.modeCon.addWidget(self.liveMode)
        self.modeCon.addWidget(self.photoMode)
        self.modeCon.setCurrentIndex(self.settings.value("currentMode", 0))

        self.liveModeBtn = None
        self.photoModeBtn = None

        self.capConLabel = None
        self.capConPathLabel = None
        self.prevCapConScroll = None
        self.prevCapCon = None
        self.prevCapConLayout = None

        self.prevCapConWidgets = []

        self.setupUi()
        self.updateCapCon()

    def initThreads(self):
        digits = []
        # The first two parameters are the position, the third is the maximum digit count
        # The fourth is a factor which the result is getting multiplied with, before returned
        # The fifth is the final format in which the result should be presented
        digits.append((575, 42,  2, 1,    "\nHigh Voltage:\n{} kv\n"))
        digits.append((575, 122, 6, 9.08, "Magnification:\n{}\n"))
        digits.append((575, 74,  2, 1,    "Working Distance:\n{} mm"))
        # Should not be changed, since the measuring relies on it

        self.liveFeedThread = CroppingReadingThread(0, "CY3014 USB, Analog 01 Capture", 720, 576,
                                                    QRect(30, 28, 510, 510), digits)
        # self.liveFeedThread = CroppingReadingThread(0, "CY3014 USB, Analog 01 Capture", 640, 480, QRect(0, 0, 480, 480), digits)
        self.camThread = CroppingThread(1, "Grabster AV 350 Capture", 640, 480, QRect(0, 0, 1000, 1000))

    def setupUi(self):
        global scalingFactor
        gridLayout = QGridLayout(self)
        gridLayout.setSpacing(0)
        gridLayout.addWidget(self.modeCon, 1, 0, 1, 1)

        self.prevCapConScroll = QScrollArea(self)
        self.prevCapConScroll.setWidgetResizable(True)
        self.prevCapConScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.prevCapConScroll.setMaximumSize(QSize(250 * scalingFactor, 16777215))
        self.prevCapConScroll.setMinimumSize(QSize(250 * scalingFactor, 0))

        self.prevCapCon = QWidget(self.prevCapConScroll)
        self.prevCapCon.setMinimumSize(QSize(220 * scalingFactor, 0))

        self.prevCapConLayout = QVBoxLayout(self.prevCapCon)

        font = QFont()

        self.capConLabel = QLabel(self.prevCapCon)
        self.capConLabel.setMaximumSize(QSize(16777215, 26 * scalingFactor))
        font.setPointSize(15)
        self.capConLabel.setFont(font)
        self.capConLabel.setAlignment(Qt.AlignTop)
        self.prevCapConLayout.addWidget(self.capConLabel)

        self.capConPathLabel = QLabel(self.prevCapCon)
        self.capConPathLabel.setMaximumSize(QSize(16777215, 26 * scalingFactor))
        font.setPointSize(8)
        self.capConPathLabel.setFont(font)
        self.capConPathLabel.setAlignment(Qt.AlignTop)
        self.prevCapConLayout.addWidget(self.capConPathLabel)

        gridLayout.addWidget(self.prevCapConScroll, 1, 1, 1, 1)

        self.capConLabel.setText(translate("Captures"))

    # Sets the current Mode to the one that you want and saves it in the settings
    def changeModeTo(self, index):
        self.modeCon.setCurrentIndex(index)
        self.settings.setValue("currentMode", self.modeCon.currentIndex())
        self.settings.sync()

    # A FileDialog starts so the user can select where they want to save the picture
    # The path is also saved in the settings, and the capture panel gets updated
    def updatePath(self):
        newPath, extension = QFileDialog.getSaveFileName(self, translate("SaveImg"), self.path, "*.png")
        return self.setPath(newPath)

    # Allows the user to change to a new folder
    def updateFolder(self):
        newPath = QFileDialog.getExistingDirectory(self, translate("ChangeFolderTitle"), self.path)
        newPath += "/"
        self.setPath(newPath)
        self.updateCapCon()

    def setPath(self, newPath):
        if newPath != '':
            self.path = newPath
            self.settings.setValue("path", self.path)
            self.settings.sync()
            return True
        return False

    # In this method all of the images of the current folder are loaded into the capture panel
    def updateCapCon(self):
        self.clearCapImages()
        newPath = '/'.join(self.path.split("/")[:-1])
        self.capConPathLabel.setText(newPath)
        self.capConPathLabel.setToolTip(newPath)

        for filename in glob.glob(newPath + '/*.png'):
            self.addCapture(filename)

        spacerItem = QSpacerItem(5, 20000, QSizePolicy.Fixed, QSizePolicy.Maximum)
        self.prevCapConScroll.setWidget(self.prevCapCon)
        self.prevCapConLayout.addItem(spacerItem)
        self.prevCapConWidgets.append(spacerItem)

    # Here every CaptureLabel which was stored in the capture panel gets deleted
    def clearCapImages(self):
        for prevCap in self.prevCapConWidgets:
            if type(prevCap) is CaptureLabel:
                self.prevCapConLayout.removeWidget(prevCap)
                prevCap.hide()
                prevCap.deleteLater()
            else:
                self.prevCapConLayout.removeItem(prevCap)

        self.prevCapConWidgets = []

    # A new capture is added to the capture panel
    def addCapture(self, file):
        img = Image.open(file)
        img.load()
        try:
            if img.info['IsREMImage'] == "1":
                newPic = CaptureLabel(self.prevCapCon)
                newPic.setImage(file, img, self.prevCapCon.width())
                newPic.clicked.connect(self.prevCapClicked)
                self.prevCapConLayout.addWidget(newPic)
                self.prevCapConWidgets.append(newPic)
        except:
            pass

    # Gets called when one of the panels in the capture panel gets clicked
    # Sets the new image and the metadata values
    def prevCapClicked(self, cl):
        self.changeModeTo(1)
        self.photoMode.updateImage(cl.image)
        self.photoMode.setMetadataValues(cl.spotSizeVal, cl.coarseVal, cl.currentVal, cl.voltageVal, cl.focusVal)

    # Frees all of the captures resources
    def close(self):
        self.liveMode.close()
        self.photoMode.close()
