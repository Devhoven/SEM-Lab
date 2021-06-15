import os
import subprocess
from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# Superclass, which contains all of the functionality of the pages
class Page(QWizardPage):

    def __init__(self, mainWindow):
        super().__init__()
        self.setStyle()
        self.setText()

    def setStyle(self):
        pass

    def applyChanges(self):
        pass

    def setText(self):
        pass


class WelcomePage(Page):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setCommitPage(True)

    def setStyle(self):
        super().setStyle()

        vertLayout = QVBoxLayout()
        vertLayout.setContentsMargins(20, 20, 20, 20)
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
        vertLayout.addWidget(pathLabel)

        self.pathLineEdit = QLineEdit("C:/ProgramFiles")
        self.pathLineEdit.setMinimumHeight(40)
        vertLayout.addWidget(self.pathLineEdit)

        self.setLayout(vertLayout)

# Responsible for the right driver settings
class DriverPage(Page):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        layout = QVBoxLayout(self)

        btn = QPushButton(self, text=translate("DriverBtnText"))
        btn.clicked.connect(self.openDriverDialog)
        layout.addWidget(btn)
        layout.setAlignment(btn, Qt.AlignHCenter)

    # Executes a cmd command which opens the driver dialog of the main cam
    def openDriverDialog(self):
        t = DriverThread()
        t.start()

# Small subclass, which runs the ffmpeg driver dialog in parallel, since otherwise the QT-Application would be on halt
class DriverThread(QThread):

    def __init__(self):
        super().__init__()

    def run(self):
        global dir
        os.chdir(dir + "/assets")
        subprocess.run(
            ["ffmpeg", "-f", "dshow", "-show_video_device_dialog", "true", "-i", "video=CY3014 USB, Analog 01 Capture"])

