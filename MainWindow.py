import os
import subprocess
from Page import *
from main import *
from PyQt5.QtWidgets import *


class MainWindow(QWizard):

    def __init__(self):
        super().__init__()

        self.setWizardStyle(QWizard.ClassicStyle)
        self.setWindowTitle(translate("WindowTitle"))

        self.welcomePage = WelcomePage(self)
        self.addPage(self.welcomePage)
        self.driverPage = DriverPage(self)
        self.addPage(self.driverPage)

        self.button(QWizard.FinishButton).clicked.connect(self.onFinish)
        self.setButtonText(QWizard.NextButton, translate("NextBtnText") + ">")
        self.setButtonText(QWizard.BackButton, "<" + translate("BackBtnText"))
        self.setButtonText(QWizard.FinishButton, translate("FinishBtnText"))
        self.setButtonText(QWizard.CancelButton, translate("CancelBtnText"))

        self.showNormal()

    def onFinish(self):
        global dir
        os.chdir(dir + "/assets")
        if self.welcomePage.camDriverCheck.isChecked():
            subprocess.run(["CamGrabber"])
        if self.welcomePage.liveFeedDriverCheck.isChecked():
            subprocess.call(["LiveGrabber"], shell=True)

    def keyPressEvent(self, event):
        # If the user presses ESC the app closes
        if event.key() == 16777216:
            self.close()
