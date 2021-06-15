from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import Widgets.StreamWidget as StreamWidget


# Takes a thread of a feed and shows it on an external window
class ExternalWindow(QMainWindow):

    def __init__(self, thread, raw=False):
        super().__init__()

        self.setWindowTitle(thread.sourceName)

        global scalingFactor
        self.setGeometry(0, 0, 512 * scalingFactor, 512 * scalingFactor)

        self.conWidget = QWidget(self)
        self.setCentralWidget(self.conWidget)
        layout = QVBoxLayout(self.conWidget)
        self.feedCon = StreamWidget.StreamWidget(thread, raw)
        layout.addWidget(self.feedCon)
        layout.setAlignment(self.feedCon, Qt.AlignHCenter)

        self.showNormal()

    # Closes the window, when Escape is pressed
    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.close()