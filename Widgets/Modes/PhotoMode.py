import numpy as np
from main import *
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Threads.RIThread import *
from PIL.ImageQt import ImageQt
from Widgets.ImageViewer import *
from Widgets.StreamWidget import *
from Widgets.MetadataWidget import *
from PIL.PngImagePlugin import PngImageFile, PngInfo

class PhotoMode(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.image = None

        self.uiContainer = parent

        self.infoField = None

        self.imageSaved = True

        self.currentImageCon = None

        self.riThread = ReadImageThread()
        self.riThread.imageLoaded.connect(self.updateImageREM)
        self.riThread.updateInfo.connect(self.setInfo)

        self.setupUi()

    def setupUi(self):
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)

        leftVerticalLayout = QVBoxLayout()
        leftVerticalLayout.setContentsMargins(0, 0, 0, 0)

        self.setupSwitchButtons(leftVerticalLayout)

        self.setupMetadataCon(leftVerticalLayout)

        self.setupAquireCon(leftVerticalLayout)

        self.setupSwapCon(leftVerticalLayout)

        self.setupCamCon(leftVerticalLayout)

        horizontalLayout.addLayout(leftVerticalLayout)

        self.currentImageCon = ImageViewer(self)
        horizontalLayout.addWidget(self.currentImageCon)
        # horizontalLayout.setAlignment(self.currentImageCon, Qt.AlignHCenter)

    def setupSwitchButtons(self, leftVerticalLayout):
        horLayout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)

        liveBtn = QPushButton()
        liveBtn.setFont(font)
        liveBtn.setText(translate("LiveMode"))
        liveBtn.setToolTip("1")
        liveBtn.setObjectName("SwitchBtn")
        liveBtn.setStyleSheet("margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + ";")
        liveBtn.clicked.connect(lambda: self.uiContainer.changeModeTo(0))

        horLayout.addWidget(liveBtn)

        photoBtn = QPushButton()
        photoBtn.setFont(font)
        photoBtn.setText(translate("PhotoMode"))
        photoBtn.setToolTip("2")
        photoBtn.setObjectName("SwitchBtn")
        photoBtn.setStyleSheet("margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + ";")
        photoBtn.setDisabled(True)

        horLayout.addWidget(photoBtn)

        leftVerticalLayout.addLayout(horLayout)

    def setupMetadataCon(self, leftVerticalLayout):
        global scalingFactor
        metadataCon = QWidget()
        metadataCon.setMinimumSize(QSize(210 * scalingFactor, 0))
        metadataCon.setMaximumSize(QSize(210 * scalingFactor, 16777215))
        metadataCon.setStyleSheet(
            ".QPushButton { margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + "; }")
        metadataConLayout = QVBoxLayout()
        metadataCon.setLayout(metadataConLayout)

        font = QFont()

        headlineLabel = QLabel(metadataCon)
        font.setPointSize(15)
        headlineLabel.setFont(font)
        headlineLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        metadataConLayout.addWidget(headlineLabel)

        font.setPointSize(12)

        # Spot size
        self.spotSizeWidget = SpotSizeWidget(metadataCon)
        metadataConLayout.addWidget(self.spotSizeWidget)

        # Coarse
        self.coarseWidget = CoarseWidget(metadataCon)
        metadataConLayout.addWidget(self.coarseWidget)

        # Current
        self.currentWidget = CurrentWidget(metadataCon)
        metadataConLayout.addWidget(self.currentWidget)

        # Voltage
        self.voltageWidget = VoltageWidget(metadataCon)
        metadataConLayout.addWidget(self.voltageWidget)

        # Dyn Focus
        self.focusWidget = FocusWidget(metadataCon)
        metadataConLayout.addWidget(self.focusWidget)

        # Reset Button
        resetBtn = QPushButton(translate("ResetBtnText"))
        resetBtn.clicked.connect(lambda: self.setMetadataValues("-1", "-1", "", "-1", "-1"))
        metadataConLayout.addWidget(resetBtn)

        headlineLabel.setText(translate("MetadataHeadline") + ":")

        leftVerticalLayout.addWidget(metadataCon)

    def setupAquireCon(self, leftVerticalLayout):
        global scalingFactor
        aquireCon = QWidget(self)
        aquireCon.setMinimumSize(QSize(210 * scalingFactor, 0))
        aquireCon.setMaximumSize(QSize(210 * scalingFactor, 16777215))
        aquireCon.setStyleSheet(
            ".QPushButton { margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + "; }")
        aquireConLayout = QVBoxLayout(aquireCon)

        font = QFont()
        font.setPointSize(15)

        headlineLabel = QLabel(aquireCon)
        headlineLabel.setFont(font)
        headlineLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        aquireConLayout.addWidget(headlineLabel)

        font.setPointSize(10)

        captureBtn = QPushButton(aquireCon)
        captureBtn.setFont(font)
        aquireConLayout.addWidget(captureBtn)

        saveBtn = QPushButton(aquireCon)
        saveBtn.setFont(font)
        aquireConLayout.addWidget(saveBtn)

        changeFolderBtn = QPushButton(aquireCon)
        changeFolderBtn.setFont(font)
        aquireConLayout.addWidget(changeFolderBtn)

        self.infoField = QLabel(aquireCon)
        self.infoField.setFont(font)
        self.infoField.setWordWrap(True)
        aquireConLayout.addWidget(self.infoField)

        headlineLabel.setText(translate("ImgCapture"))
        captureBtn.setText(translate("CaptureImg"))
        saveBtn.setText(translate("SaveImg"))
        changeFolderBtn.setText(translate("ChangeFolderTitle"))
        self.setInfo(translate("ReadyForImg"))

        captureBtn.clicked.connect(lambda: self.scanImage())
        saveBtn.clicked.connect(lambda: self.saveImage())
        changeFolderBtn.clicked.connect(lambda: self.uiContainer.updateFolder())

        leftVerticalLayout.addWidget(aquireCon)

    def setupSwapCon(self, leftVerticalLayout):
        global scalingFactor
        swapCon = QWidget(self)
        swapCon.setMinimumSize(QSize(210 * scalingFactor, 0))
        swapCon.setMaximumSize(QSize(210 * scalingFactor, 16777215))
        swapCon.setStyleSheet(
            ".QPushButton { margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + "; }")
        swapConLayout = QVBoxLayout()
        swapCon.setLayout(swapConLayout)

        font = QFont()
        font.setPointSize(15)

        headlineLabel = QLabel(swapCon)
        headlineLabel.setFont(font)
        headlineLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        swapConLayout.addWidget(headlineLabel)

        font.setPointSize(10)

        horizontalLayout = QHBoxLayout()

        rollUpBtn = QPushButton(swapCon)
        rollUpBtn.setFont(font)
        horizontalLayout.addWidget(rollUpBtn)

        rollDownBtn = QPushButton(swapCon)
        rollDownBtn.setFont(font)
        horizontalLayout.addWidget(rollDownBtn)

        swapConLayout.addLayout(horizontalLayout)

        squishBtn = QPushButton(swapCon)
        squishBtn.setFont(font)
        swapConLayout.addWidget(squishBtn)

        spacer = QSpacerItem(1, 1, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        swapConLayout.addSpacerItem(spacer)

        leftVerticalLayout.addWidget(swapCon)

        headlineLabel.setText(translate("RepairHeadline"))
        rollUpBtn.setText(translate("RollUp"))
        rollDownBtn.setText(translate("RollDown"))
        squishBtn.setText("Squish")

        rollUpBtn.clicked.connect(lambda: self.rollUpImage())
        rollDownBtn.clicked.connect(lambda: self.rollDownImage())
        squishBtn.clicked.connect(lambda: self.squishImg())

    def squishImg(self, factor=0.9420):
        if self.image is not None:
            newImg = cv2.resize(self.image, dsize=(2048, int(2048 * factor)), interpolation=cv2.INTER_LANCZOS4)
            self.updateImage(newImg)

    def setupCamCon(self, leftVerticalLayout):
        global scalingFactor

        conWidget = QWidget(self)
        conWidget.setFixedSize(QSize(210 * scalingFactor, 210 * scalingFactor))

        conWidgetLayout = QVBoxLayout(conWidget)

        camCon = StreamWidget(self.uiContainer.camThread)
        camCon.setFixedSize(190 * scalingFactor, 190 * scalingFactor)
        camCon.setMaximumSize(190 * scalingFactor, 190 * scalingFactor)
        camCon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        conWidgetLayout.addWidget(camCon)
        conWidgetLayout.setAlignment(camCon, Qt.AlignHCenter)

        leftVerticalLayout.addWidget(conWidget)

    # Sets all of the metadata values
    def setMetadataValues(self, spotSizeVal, coarseVal, currentVal, voltageVal, focusVal):
        self.spotSizeWidget.setValue(spotSizeVal)

        self.coarseWidget.reset()
        self.coarseWidget.setValue(coarseVal)

        self.currentWidget.setValue(currentVal)

        self.voltageWidget.reset()
        self.voltageWidget.setValue(voltageVal)

        self.focusWidget.reset()
        self.focusWidget.setValue(focusVal)

    def updateImageREM(self, newImage):
        self.updateImage(newImage)
        self.imageSaved = False

    def updateImage(self, newImage):
        self.checkImageSaved()
        self.image = newImage
        self.setImageNP(newImage.copy())

    def setImageNP(self, newImage):
        im = Image.fromarray(newImage)
        im = im.convert("RGB")
        qix = ImageQt(im)
        pix = QPixmap.fromImage(qix)
        self.currentImageCon.updateImage(pix.scaled(2050, 2050, Qt.KeepAspectRatio))

    def checkImageSaved(self):
        if not self.imageSaved:
            saveDialog = QMessageBox()
            saveDialog.setWindowTitle(translate("Title"))
            saveDialog.setText(translate("ImgNotSavedInfo"))
            saveDialog.setStandardButtons(QMessageBox.Save | QMessageBox.Ok)
            saveDialog.buttonClicked.connect(self.messageBoxClicked)
            saveDialog.exec()

    def messageBoxClicked(self, btn):
        if btn.text() == "Save":
            self.saveImage()
        else:
            self.imageSaved = True

    # Saves the image that is currently in the image viewer
    # Saves all of the metadata with it
    def saveImage(self):
        self.checkMetadataCorrect()

    # Creates a dialog box which asks the user if all of the metadata values are correct
    def checkMetadataCorrect(self):
        mdDialog = QMessageBox()
        mdDialog.setWindowTitle(translate("Title"))
        mdDialog.setText(translate("MetadataCorrectQuestion"))
        mdDialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mdDialog.buttonClicked.connect(self.metadataBoxClicked)
        mdDialog.exec()

    def metadataBoxClicked(self, btn):
        if btn.text() == "&Yes" and self.uiContainer.updatePath():
            im = Image.fromarray(self.image)
            im = im.convert("RGB")
            metadata = PngInfo()

            metadata.add_text("IsREMImage", "1")

            metadata.add_text("SpotSize", str(self.spotSizeWidget.getValue()))

            metadata.add_text("Coarse", self.coarseWidget.getValue())

            metadata.add_text("Current", self.currentWidget.getValue())

            metadata.add_text("Voltage", self.voltageWidget.getValue())

            metadata.add_text("Focus", self.focusWidget.getValue())

            im.save(self.uiContainer.path, pnginfo=metadata)
            self.uiContainer.updateCapCon()
            self.imageSaved = True

    def scanImage(self):
        self.checkImageSaved()
        self.setInfo(translate("PressBtnInfo"))
        self.riThread.startGetImage()

    def rollUpImage(self):
        self.image = np.roll(self.image, 1023, axis=1)
        self.image = np.roll(self.image, 120, axis=0)
        self.setImageNP(self.image)

    def rollDownImage(self):
        self.image = np.roll(self.image, -1023, axis=1)
        self.image = np.roll(self.image, -120, axis=0)
        self.setImageNP(self.image)

    def setInfo(self, newText):
        if newText == "1":
            self.riThread.close()
            self.infoField.setText(translate("ImgRdyInfo"))
        else:
            self.infoField.setText(newText)

    def keyPressEvent(self, event):
        # When the user pressed the enter key, the image scan starts
        if event.key() == 16777220:
            self.scanImage()

    def closeEvent(self, event):
        self.checkImageSaved()
