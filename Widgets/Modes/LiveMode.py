import cv2
from main import *
from Widgets.LUTList import *
from Widgets.StreamWidget import *

class LiveMode(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.uiContainer = parent

        self.liveDataLabel = None
        self.liveFeedCon = None

        self.camCon = None

        self.camInfoLabel = None

        self.setupUi()

    def setupUi(self):
        global scalingFactor
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)

        leftVerticalLayout = QVBoxLayout()
        leftVerticalLayout.setContentsMargins(0, 0, 0, 0)

        self.setupSwitchButtons(leftVerticalLayout)

        self.setupInfoCon(leftVerticalLayout)

        self.setupLUTCon(leftVerticalLayout)

        self.setupCamCon(leftVerticalLayout)

        horizontalLayout.addLayout(leftVerticalLayout)

        self.liveFeedCon = MeasureStreamWidget(self.uiContainer.liveFeedThread)
        self.liveFeedCon.setMaximumSize(1024 * scalingFactor, 1024 * scalingFactor)
        self.liveFeedCon.thread.info.connect(self.camInfoLabel.setText)

        horizontalLayout.addWidget(self.liveFeedCon)
        horizontalLayout.setAlignment(self.liveFeedCon, Qt.AlignHCenter)

    def setupInfoCon(self, leftVerticalLayout):
        global scalingFactor
        font = QFont()

        infoCon = QWidget(self)
        infoCon.setMaximumSize(210 * scalingFactor, 16777215)
        infoConLayout = QVBoxLayout(infoCon)

        camInfoTitle = QLabel(translate("CamInfoTitle") + ":")
        font.setPointSize(15)
        camInfoTitle.setFont(font)
        infoConLayout.addWidget(camInfoTitle)

        self.camInfoLabel = QLabel()
        font.setPointSize(12)
        self.camInfoLabel.setFont(font)
        infoConLayout.addWidget(self.camInfoLabel)

        leftVerticalLayout.addWidget(infoCon)

    def setupLUTCon(self, leftVerticalLayout):
        global scalingFactor
        lutCon = QWidget()
        lutCon.setMinimumSize(QSize(210 * scalingFactor, 0))
        lutCon.setMaximumSize(QSize(210 * scalingFactor, 16777215))
        lutCon.setStyleSheet(
            ".QPushButton { margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor) + "; }")
        lutConLayout = QVBoxLayout()
        lutCon.setLayout(lutConLayout)

        self.lutList = []
        self.lutList.append(LUTItem("None", None))
        self.lutList.append(LUTItem("Bone", cv2.COLORMAP_BONE))
        self.lutList.append(LUTItem("Cool", cv2.COLORMAP_COOL))
        self.lutList.append(LUTItem("Hot", cv2.COLORMAP_HOT))
        self.lutList.append(LUTItem("HSV", cv2.COLORMAP_HSV))
        self.lutList.append(LUTItem("Jet", cv2.COLORMAP_JET))
        self.lutList.append(LUTItem("Ocean", cv2.COLORMAP_OCEAN))
        self.lutList.append(LUTItem("Pink", cv2.COLORMAP_PINK))
        self.lutList.append(LUTItem("Rainbow", cv2.COLORMAP_RAINBOW))
        self.lutList.append(LUTItem("Autumn", cv2.COLORMAP_AUTUMN))
        self.lutList.append(LUTItem("Summer", cv2.COLORMAP_SUMMER))
        self.lutList.append(LUTItem("Spring", cv2.COLORMAP_SPRING))
        self.lutList.append(LUTItem("Winter", cv2.COLORMAP_WINTER))

        lutComboBox = LUTList(self.lutList)
        lutComboBox.currentIndexChanged.connect(self.setLUT)
        lutConLayout.addWidget(lutComboBox)

        spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        lutConLayout.addSpacerItem(spacerItem)

        leftVerticalLayout.addWidget(lutCon)

    def setLUT(self, index):
        self.liveFeedCon.thread.cvLUT = self.lutList[index].cvType

    def setupCamCon(self, leftVerticalLayout):
        global scalingFactor

        conWidget = QWidget(self)
        conWidget.setMinimumSize(QSize(210 * scalingFactor, 0))
        conWidget.setMaximumSize(QSize(210 * scalingFactor, 210 * scalingFactor))

        conWidgetLayout = QVBoxLayout(conWidget)

        self.camCon = StreamWidget(self.uiContainer.camThread)
        self.camCon.setFixedSize(190 * scalingFactor, 190 * scalingFactor)
        self.camCon.setMaximumSize(190 * scalingFactor, 190 * scalingFactor)
        self.camCon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        conWidgetLayout.addWidget(self.camCon)
        conWidgetLayout.setAlignment(self.camCon, Qt.AlignHCenter)

        leftVerticalLayout.addWidget(conWidget)

    def setupSwitchButtons(self, leftVerticalLayout):
        global scalingFactor
        horLayout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)

        liveBtn = QPushButton()
        liveBtn.setFont(font)
        liveBtn.setText(translate("LiveMode"))
        liveBtn.setToolTip("1")
        liveBtn.setObjectName("SwitchBtn")
        liveBtn.setStyleSheet("margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor))
        liveBtn.setDisabled(True)

        horLayout.addWidget(liveBtn)

        photoBtn = QPushButton()
        photoBtn.setFont(font)
        photoBtn.setText(translate("PhotoMode"))
        photoBtn.setToolTip("2")
        photoBtn.setObjectName("SwitchBtn")
        photoBtn.setStyleSheet("margin-top: 5; margin-bottom: 5; height: " + str(30 * scalingFactor))
        photoBtn.clicked.connect(lambda: self.uiContainer.changeModeTo(1))

        horLayout.addWidget(photoBtn)

        leftVerticalLayout.addLayout(horLayout)

    def close(self):
        self.liveFeedCon.close()
        self.camCon.close()
