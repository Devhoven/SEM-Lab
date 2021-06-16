import os
import subprocess
from main import *
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class WelcomePage(QWizardPage):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        vertLayout = QVBoxLayout()

        font = QFont()
        font.setPointSize(12)

        welcomeLabel = QLabel(translate("WelcomeMessage"))
        welcomeLabel.setWordWrap(True)
        welcomeLabel.setFont(font)
        vertLayout.addWidget(welcomeLabel)

        self.setLayout(vertLayout)


class SoftwarePage(QWizardPage):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setCommitPage(True)
        self.setStyle()

    def setStyle(self):
        vertLayout = QVBoxLayout()
        self.setLayout(vertLayout)

        font = QFont()

        font.setPointSize(13)
        headlineLabel = QLabel(translate("Headline"))
        headlineLabel.setFont(font)
        vertLayout.addWidget(headlineLabel)

        font.setPointSize(10)

        self.guiCheck = QCheckBox(translate("SEMCheckboxText"))
        self.guiCheck.setFont(font)
        self.guiCheck.setChecked(True)
        vertLayout.addWidget(self.guiCheck)

        self.camDriverCheck = QCheckBox(translate("CamCheckboxText"))
        self.camDriverCheck.setFont(font)
        self.camDriverCheck.setChecked(True)
        vertLayout.addWidget(self.camDriverCheck)

        self.liveFeedDriverCheck = QCheckBox(translate("LiveFeedCheckboxText"))
        self.liveFeedDriverCheck.setFont(font)
        self.liveFeedDriverCheck.setChecked(True)
        vertLayout.addWidget(self.liveFeedDriverCheck)

        pathLabel = QLabel("\n" + translate("PathText"))
        pathLabel.setFont(font)
        vertLayout.addWidget(pathLabel)

        pathLayout = QHBoxLayout()

        self.pathDisplay = QLabel("C:/ProgramFiles")
        self.pathDisplay.setFont(font)
        self.pathDisplay.setStyleSheet("border: 1px solid black;")
        pathLayout.addWidget(self.pathDisplay)
        pathButton = QPushButton(translate("SelectFolderText"))
        pathButton.setFont(font)
        pathButton.clicked.connect(self.changePath)
        pathLayout.addWidget(pathButton)
        vertLayout.addLayout(pathLayout)

    def changePath(self):
        self.pathDisplay.setText(QFileDialog.getExistingDirectory(self, "Select Directory"))


# Responsible for the right driver settings
class DriverPage(QWizardPage):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        vertLayout = QVBoxLayout()

        font = QFont()
        font.setPointSize(11)

        headlineLabel = QLabel(translate("DriverPageHeadlineText"))
        headlineLabel.setFont(font)
        headlineLabel.setWordWrap(True)
        vertLayout.addWidget(headlineLabel)

        horLayout = QHBoxLayout()

        btn = QPushButton(self, text=translate("DriverBtnText"))
        btn.clicked.connect(self.openDriverDialog)
        horLayout.addWidget(btn)

        manualImageBtn = QPushButton(translate("OpenImageText"))
        manualImageBtn.clicked.connect(self.openImage)
        horLayout.addWidget(manualImageBtn)

        vertLayout.addLayout(horLayout)

        manualLabel = QLabel(translate("ManualText"))
        manualLabel.setWordWrap(True)
        vertLayout.addWidget(manualLabel)

        self.setLayout(vertLayout)

    # Executes a cmd command which opens the driver dialog of the main cam
    def openDriverDialog(self):
        DriverThread(self).start()

    # Opens the properties image in the default system viewer
    def openImage(self):
        DriverImageThread(self).start()

# Small subclass, which runs the ffmpeg driver dialog in parallel, since otherwise the QT-Application would be on halt
class DriverThread(QThread):

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        global dir
        os.chdir(dir + "/assets")
        subprocess.run(
            ["ffmpeg", "-f", "dshow", "-show_video_device_dialog", "true", "-i", "video=CY3014 USB, Analog 01 Capture"])


# Small subclass, which runs the default system viewer in parallel, since otherwise the Wizard would stop working,
# until the viewer is closed again
class DriverImageThread(QThread):

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        global dir
        img = Image.open(dir + '/assets/Properties.png')
        img.show()