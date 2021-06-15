import os
import subprocess
from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Creates another thread where the driver settings can be edited
class DriverDialogThread(QThread):

    def __init__(self, parent, camName):
        super().__init__(parent)

        self.camName = camName

    # Uses ffmpeg to open the driver dialog via the cmd
    def run(self):
        global dir
        os.chdir(dir + "/assets")
        subprocess.run(["ffmpeg", "-f", "dshow", "-show_video_device_dialog", "true", "-i", "video=" + self.camName])