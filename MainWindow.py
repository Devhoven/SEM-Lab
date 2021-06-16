import os
import subprocess
from Page import *
from main import *
from Threads import *
from PyQt5.QtWidgets import *


class MainWindow(QWizard):

    def __init__(self):
        super().__init__()

        self.setWizardStyle(QWizard.ClassicStyle)
        self.setWindowTitle(translate("WindowTitle"))
        self.setWindowIcon(QIcon("assets/Icon.png"))

        welcomePage = WelcomePage(self)
        self.softwarePage = SoftwarePage(self)
        self.progressPage = ProgressPage(self)
        self.driverPage = DriverPage(self)

        self.addPage(welcomePage)
        self.addPage(self.softwarePage)
        self.addPage(self.progressPage)
        self.addPage(self.driverPage)

        self.button(QWizard.CommitButton).clicked.connect(self.onCommit)
        self.setButtonText(QWizard.NextButton, translate("NextBtnText") + ">")
        self.setButtonText(QWizard.BackButton, "<" + translate("BackBtnText"))
        self.setButtonText(QWizard.FinishButton, translate("FinishBtnText"))
        self.setButtonText(QWizard.CancelButton, translate("CancelBtnText"))
        self.setButtonText(QWizard.CommitButton, "Install")

        self.show()


    # Executes the setups if the boxes are checked
    # And installs the software itself at the end
    def onCommit(self):
        global dir
        os.chdir(dir + "/assets")
        if self.softwarePage.camDriverCheck.isChecked():
            subprocess.run(["CamGrabber"])
        if self.softwarePage.liveFeedDriverCheck.isChecked():
            subprocess.call(["LiveGrabber"], shell=True)

        if self.softwarePage.guiCheck.isChecked():
            downloadThread = DownloadThread(self, self.softwarePage.pathDisplay.text())
            downloadThread.progressChanged.connect(self.progressPage.setProgress)
            downloadThread.start()


    def keyPressEvent(self, event):
        # If the user presses ESC the app closes
        if event.key() == 16777216:
            self.close()
