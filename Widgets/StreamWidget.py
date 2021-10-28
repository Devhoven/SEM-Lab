import math

import cv2
from main import *
from ExternalWindow import *
from Threads.Thread import *
from Threads.DriverDialogThread import *


class StreamWidget(QLabel):

    # source is the source of the video stream
    # width and height define the width and height of the input stream
    # cropRect is a QRect which crops the final Image
    def __init__(self, thread, raw=False):
        super().__init__()

        self.originalImage = None
        self.image = QPixmap(1, 1)

        # Ensures, that you can't open more than one window from one stream
        # You can still click on the new stream and open another one, but that's fine
        self.newWindow = None

        self.thread = thread
        if not raw:
            self.thread.changePixmap.connect(self.updatePixmap)
        else:
            self.thread.changePixmapRaw.connect(self.updatePixmap)

    # This method gets called when the stream got a new picture from the video stream
    # It updates the current image
    def updatePixmap(self, image):
        self.setMinimumSize(1, 1)
        self.originalImage = image
        self.image = image.scaled(self.size().height(), self.size().height(), Qt.KeepAspectRatio)
        self.setPixmap(self.image)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        driverAction = menu.addAction(translate("OpenDriverAction"))
        driverAction.triggered.connect(lambda: self.openDriverDialog(self.thread.sourceName))

        externalWindowAction = menu.addAction(translate("OpenExternalWindowAction"))
        externalWindowAction.triggered.connect(lambda: self.openExternalWindow(False))

        externalWindowActionRaw = menu.addAction(translate("OpenExternalWindowRawAction"))
        externalWindowActionRaw.triggered.connect(lambda: self.openExternalWindow(True))

        menu.exec_(event.globalPos())

    # Executes a cmd command which opens the driver dialog of the main cam
    def openDriverDialog(self, camName):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(translate("VideoProcAmpInformation"))
        msg.exec_();
        camThread = DriverDialogThread(self, camName)
        camThread.start()

    # Opens a new window which only shows the thread
    def openExternalWindow(self, raw):
        self.newWindow = ExternalWindow(self.thread, raw)

    # This method will be called when the window gets closed
    # It is responsible to free all captured resources
    def close(self):
        self.thread.close()
        self.deleteLater()


# Adds an option to the context menu, which allows the user to measure
class MeasureStreamWidget(StreamWidget):

    def __init__(self, thread, factor=1):
        super().__init__(thread)

        self.magnification = 1
        self.thread.info.connect(self.setMagnification)

        self.measureMode = 0

        self.factor = factor

        self.mouseMoved = False
        self.grabbing = False

        self.innerPoint = QPoint(0, 0)
        self.outerPoint = QPoint(0, 0)
        self.oldMousePos = QPoint(0, 0)
        self.currentMousePos = QPoint(0, 0)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        driverAction = menu.addAction(translate("OpenDriverAction"))
        driverAction.triggered.connect(lambda: self.openDriverDialog(self.thread.sourceName))

        externalWindowAction = menu.addAction(translate("OpenExternalWindowAction"))
        externalWindowAction.triggered.connect(self.openExternalWindow)

        externalWindowRawAction = menu.addAction(translate("OpenExternalWindowRawAction"))
        externalWindowRawAction.triggered.connect(lambda: self.openExternalWindow(True))

        measureRectAct = menu.addAction(translate("MeasureRectAction"))
        measureRectAct.triggered.connect(lambda: self.setMeasureMode(0))

        measureLineAct = menu.addAction(translate("MeasureCircleAction"))
        measureLineAct.triggered.connect(lambda: self.setMeasureMode(1))

        menu.exec_(event.globalPos())

    def setMagnification(self, infoText):
        self.magnification = [int(s) for s in infoText.split() if s.isdigit()][1] / 9.08

    def setMeasureMode(self, mode):
        self.measureMode = mode

    # Checks if the mouse is in the currently measure tool and sets the grabbing bool
    def mousePressEvent(self, event):
        # If anything was drawn yet
        if self.innerPoint != self.outerPoint:
            # If the currently used shape was a rectangle
            if self.measureMode == 0:
                # Checking if the cursor is in the Rect
                topLeft = QPoint(min(self.innerPoint.x(), self.outerPoint.x()), min(self.innerPoint.y(), self.outerPoint.y()))
                bottomRight = QPoint(max(self.innerPoint.x(), self.outerPoint.x()), max(self.innerPoint.y(), self.outerPoint.y()))
                currentPos = event.pos()
                if currentPos.x() >= topLeft.x() and currentPos.x() <= bottomRight.x() and \
                   currentPos.y() >= topLeft.y() and currentPos.y() <= bottomRight.y():
                    self.grabbing = True
            # Triggers if the used shape was a circle
            else:
                # Checks if the cursor is in the circle
                distance = self.distance(self.innerPoint, self.outerPoint)
                distanceToMouse = self.distance(self.innerPoint, event.pos())
                if distanceToMouse <= distance:
                    self.grabbing = True

    def mouseReleaseEvent(self, event):
        if not self.mouseMoved and not self.grabbing:
            self.oldMousePos = self.currentMousePos
            self.innerPoint = self.outerPoint

        self.mouseMoved = False
        self.grabbing = False

    def mouseMoveEvent(self, event):
        # If the mouse starts to move, the oldMousePos is set here
        if not self.mouseMoved:
            # If the user is not inside of an old shape
            if not self.grabbing:
                self.oldMousePos = event.pos()
                self.innerPoint = event.pos()
            else:
                self.oldMousePos = event.pos()
                self.currentMousePos = event.pos()

        self.mouseMoved = True

        if not self.grabbing:
            self.currentMousePos = event.pos()
            self.outerPoint = event.pos()
        else:
            # Moves the grabbed shape around
            self.oldMousePos = self.currentMousePos
            self.currentMousePos = event.pos()
            vel = self.currentMousePos - self.oldMousePos
            self.innerPoint += vel
            self.outerPoint += vel

        # Calling repaint here, so everything moves smoother when measuring
        self.repaint()

    # repaint has to be called, since the painter is used for this label
    def updatePixmap(self, image):
        super().updatePixmap(image)
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QRectF(0, 0, self.height(), self.height()), self.image, QRectF(0, 0, self.image.width(), self.image.height()))
        # Gets the currently set color
        global settings
        pen = QPen(QColor(settings.value("LineColor", "#DDD00D")), 3)
        painter.setPen(pen)
        if self.oldMousePos != self.outerPoint:
            if self.measureMode == 0:
                self.drawRect(painter)
            else:
                self.drawCircle(painter)

    def drawLine(self, painter):
        if self.innerPoint.y() < self.outerPoint.y():
            painter.drawText(self.innerPoint.x(), self.innerPoint.y() - 5, self.getDist(self.distance(self.innerPoint, self.outerPoint)))
        else:
            painter.drawText(self.innerPoint.x(), self.innerPoint.y() + 20, self.getDist(self.distance(self.innerPoint, self.outerPoint)))

        painter.drawLine(self.innerPoint.x(), self.innerPoint.y(),
                         self.outerPoint.x(), self.outerPoint.y())

    def drawRect(self, painter):
        painter.drawRect(self.innerPoint.x(), self.innerPoint.y(),
                         self.outerPoint.x() - self.innerPoint.x(),
                         self.outerPoint.y() - self.innerPoint.y())

        width = self.outerPoint.x() - self.innerPoint.x()
        height = self.outerPoint.y() - self.innerPoint.y()

        if self.innerPoint.y() < self.outerPoint.y():
            painter.drawText(self.innerPoint.x() + width / 2, self.innerPoint.y() - 5,
                             self.getDist(abs(width * self.factor)))
        else:
            painter.drawText(self.innerPoint.x() + width / 2, self.outerPoint.y() - 5,
                             self.getDist(abs(width * self.factor)))

        if self.innerPoint.x() < self.outerPoint.x():
            painter.drawText(self.outerPoint.x() + 5, self.innerPoint.y() + height / 2,
                             self.getDist(abs(height * self.factor)))
        else:
            painter.drawText(self.innerPoint.x() + 5, self.innerPoint.y() + height / 2,
                             self.getDist(abs(height * self.factor)))

        self.drawLine(painter)

    def drawCircle(self, painter):
        radius = self.distance(self.innerPoint, self.outerPoint)
        painter.drawEllipse(self.innerPoint, radius, radius)
        painter.drawEllipse(self.innerPoint, 3, 3)
        self.drawLine(painter)

    # Calculates the euclidian distance, since the manhattanDistance from the QPoint Object, is not what we want in this case
    def distance(self, p1, p2):
        between = p2 - p1
        return math.sqrt(between.x() * between.x() + between.y() * between.y())

    # Calculates the real distance and formats it correctly
    def getDist(self, distance):
        distance = distance / self.magnification * 90_000 / 1962

        if distance > 1000:
            return str(round(distance / 1000, 2)) + " mm"
        else:
            return str(round(distance, 1)) + " μm"

