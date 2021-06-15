import os
import subprocess
from Page import *
from main import *
from PyQt5.QtWidgets import *
import urllib.request
from urllib.request import urlretrieve
import zipfile


class MainWindow(QWizard):

    def __init__(self):
        super().__init__()

        self.setWizardStyle(QWizard.ClassicStyle)
        self.setWindowTitle(translate("WindowTitle"))
        self.setMinimumSize(950, 500)

        self.welcomePage = WelcomePage(self)
        self.addPage(self.welcomePage)
        self.driverPage = DriverPage(self)
        self.addPage(self.driverPage)

        self.button(QWizard.CommitButton).clicked.connect(self.onCommit)
        self.setButtonText(QWizard.NextButton, translate("NextBtnText") + ">")
        self.setButtonText(QWizard.BackButton, "<" + translate("BackBtnText"))
        self.setButtonText(QWizard.FinishButton, translate("FinishBtnText"))
        self.setButtonText(QWizard.CancelButton, translate("CancelBtnText"))

        self.showNormal()


    # Executes the setups if the boxes are checked
    # And installs the software itself at the end
    def onCommit(self):
        global dir
        os.chdir(dir + "/assets")
        if self.welcomePage.camDriverCheck.isChecked():
            subprocess.run(["CamGrabber"])
        if self.welcomePage.liveFeedDriverCheck.isChecked():
            subprocess.call(["LiveGrabber"], shell=True)

        if self.welcomePage.guiCheck.isChecked():
            # Downloads the zip from github
            path = self.welcomePage.pathLineEdit.text()
            urllib.request.urlretrieve("https://github.com/Devhoven/SEM-Lab/releases/download/1.0/SEM.Lab.zip",
                                       path + "/SEM-Lab.zip")

            # Unpacks the zip to the folder
            with zipfile.ZipFile(path + "/SEM-Lab.zip", 'r') as zip_ref:
                zip_ref.extractall(path)

            # Deletes the file again
            os.remove(path + "/SEM-Lab.zip")


    def keyPressEvent(self, event):
        # If the user presses ESC the app closes
        if event.key() == 16777216:
            self.close()
