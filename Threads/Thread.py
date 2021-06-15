import cv2
from PIL import Image
from time import sleep
from ReadImage import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage
from timeit import default_timer as timer


# This class is responsible for processing the video stream
# Every instance runs on a different thread
class Thread(QThread):

    changePixmap = pyqtSignal(QPixmap)
    changePixmapRaw = pyqtSignal(QPixmap)

    # "sourceName" is the system name for the camera, used for the ffmpeg driver dialog
    def __init__(self, source, sourceName, width, height):
        super(Thread, self).__init__()
        # Tells the thread when to stop
        self.threadActive = True

        self.sourceName = sourceName

        self.cvLUT = None

        self.capture = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        # Sets the frame width and height
        # If this it not set, the picture won't be as clean
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def run(self):
        while self.threadActive:
            # frame contains the next frame
            # ret contains a bool, which tells the computer if the new frame is valid
            ret, frame = self.capture.read()
            if ret:
                # Here the frame gets processed, it is not implemented in the default Thread class, but in the subclasses
                height, width, ch = frame.shape
                self.changePixmapRaw.emit(QPixmap(QImage(bytes(frame.data), width, height, ch * width, QImage.Format_RGB888)))
                frame = self.processImage(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, ch = frame.shape
                img = QPixmap(QImage(bytes(frame.data), width, height, ch * width, QImage.Format_RGB888))
                # Checking again if the thread is still active, because if not and this thread emits an signal
                # the GUI is going to crash
                if self.threadActive:
                    self.changePixmap.emit(img)

            # If there is a problem and the program does not close correctly, this small delay ensures, that there won't
            # be a thread that burns your pc
            sleep(0.00001)

    def processImage(self, frame):
        if self.cvLUT is None:
            return frame
        else:
            return cv2.applyColorMap(frame, self.cvLUT)

    # Releases the resources
    def close(self):
        # The thread gets closed
        self.threadActive = False
        # Waiting till the run() method stops
        self.wait()
        self.capture.release()


class CroppingThread(Thread):

    def __init__(self, source, sourceName, width, height, cropRect):
        self.cropRect = cropRect
        super().__init__(source, sourceName, width, height)

    def processImage(self, frame):
        return self.cropImg(super().processImage(frame), self.cropRect.x(), self.cropRect.y(), self.cropRect.width(), self.cropRect.height())

    def cropImg(self, img, x, y, width, height):
        return img[y:y + height, x:x + width]


class CroppingReadingThread(CroppingThread):

    info = pyqtSignal(str)

    def __init__(self, source, sourceName, width, height, cropRect, digits):
        super().__init__(source, sourceName, width, height, cropRect)

        self.percentage = 0

        self.digits = digits

        # Die Bilder der Zahlen von 0-9
        self.images = []
        for i in range(10):
            self.images.append(self.threshold(cv2.imread("assets/Numbers/" + str(i) + ".png", 0)))

    def processImage(self, frame):
        treshImg = self.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        result = ""
        for digit in self.digits:
            result += digit[4].format(int(self.getNumber(treshImg, digit[0], digit[1], digit[2]) * digit[3]))

        strip = self.cropImg(treshImg, 684, 42, 1, 442)
        # A one pixel wide stripe is cut out of the image, it is used to get the percentage of the scanning process
        n_white_pix = cv2.countNonZero(strip)
        percentage = int((n_white_pix / 442) * 100)

        # If a new step is reached, it is telling the rest of the program
        if percentage > self.percentage or percentage == 0:
            setPercentage(percentage)
            self.percentage = percentage

        self.info.emit(result)

        return super().processImage(frame)

    # Every pixel in the image which is smaller than the threshold is set to 0, every other pixel is set to 255
    def threshold(self, array, th=150):
        if array is not None:
            array[array <= th] = 0
            array[array > th] = 255
        return array

    # threshImg is the tresholded image from the REM
    # x and y make up the position of the top left corner of the leftmost number
    # count is the maximum count of digits
    def getNumber(self, treshImg, x, y, count):
        number = "0"
        for i in range(count):
            # Every number is 10 x 14 pixels big
            img = self.cropImg(treshImg, x, y, 10, 14)
            # Every 2 spaces there are instead of 6 pixels *7* pixels space
            if i % 2 == 1:
                x += 17
            else:
                x += 16
            # If less than 10 white Pixels are in the image, it probably does not represent a number
            # 10 is an arbitrary number, which accounts for noise
            if cv2.countNonZero(img) < 10:
                continue
            number += str(self.getIndex(img))

        return int(number)

    # Takes an image and compares it with the screenshot, so it returns which number most probably is
    # represented in the image
    def getIndex(self, img):
        maxVal = 0
        maxIndex = 0
        for i in range(10):
            val = self.compareImg(img, self.images[i])
            if val > maxVal:
                maxVal = val
                maxIndex = i

        return maxIndex

    # Returns the number of pixels which have the same color on the same position
    def compareImg(self, img1, img2):
        return sum((img1 == 255)[img2 == 255])