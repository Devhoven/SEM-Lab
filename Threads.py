import os
import zipfile
import requests
import subprocess
from main import *
import numpy as np
from PIL import Image
import urllib.request
from PyQt5.QtCore import *


# Small subclass, which runs the ffmpeg driver dialog in parallel, since otherwise the QT-Application would be on halt
class DriverThread(QThread):

    def run(self):
        global dir
        os.chdir(dir + "/assets")
        subprocess.run(
            ["ffmpeg", "-f", "dshow", "-show_video_device_dialog", "true", "-i", "video=CY3014 USB, Analog 01 Capture"])


# Small subclass, which runs the default system viewer in parallel, since otherwise the Wizard would stop working,
# until the viewer is closed again
class DriverImageThread(QThread):

    def run(self):
        global dir
        img = Image.open(dir + '/assets/Properties.png')
        img.show()


class DownloadThread(QThread):

    progressChanged = pyqtSignal(int)

    def __init__(self, parent, path):
        super().__init__(parent)
        self.path = path

    def run(self):
        self.progressChanged.emit(0)
        # Downloads the zip from github
        path = self.path

        # Stolen from StackOverflow: https://stackoverflow.com/a/37573701
        # Modified a bit
        url = "https://github.com/Devhoven/SEM-Lab/releases/download/1.0/SEM.Lab.zip"  # big file test
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 2048  # 2 Kibibytes
        count = 0
        with open(path + "/SEM-Lab.zip", 'wb') as file:
            for data in response.iter_content(block_size):
                count += len(data)
                self.progressChanged.emit(int(count / total_size_in_bytes * 99))
                file.write(data)

        # Unpacks the zip to the folder
        with zipfile.ZipFile(path + "/SEM-Lab.zip", 'r') as zip_ref:
            zip_ref.extractall(path)

        # Deletes the file again
        os.remove(path + "/SEM-Lab.zip")

        self.progressChanged.emit(100)
