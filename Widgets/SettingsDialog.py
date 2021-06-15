import serial
from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import ReadImage


class SettingsDialog(QDialog):

    def __init__(self, parent, settings):
        super().__init__(parent, Qt.WindowCloseButtonHint)

        self.settings = settings

        self.setWindowTitle(translate("Settings"))

        self.setupUi()

        self.activateWindow()

    def setupUi(self):
        vertLayout = QVBoxLayout(self)

        backgroundColorBtn = QPushButton(translate("ChooseBackgroundColor"))
        backgroundColorBtn.clicked.connect(lambda: self.setColor("PhotoBackgroundColor"))

        lineColorBtn = QPushButton(translate("ChooseLineColor"))
        lineColorBtn.clicked.connect(lambda: self.setColor("LineColor"))

        portComboBox = QComboBox()

        availablePorts = self.getAvailablePorts()
        for port in availablePorts:
            portComboBox.addItem(port)

        portComboBox.currentTextChanged.connect(self.changePort)
        currentPort = self.settings.value("Port", "COM4")
        portComboBox.setCurrentIndex(portComboBox.findText(currentPort))

        vertLayout.addWidget(QLabel(translate("SEMPort") + ":"))
        vertLayout.addWidget(portComboBox)

        languageLayout = QVBoxLayout()
        languageLabel = QLabel(translate("Restart"))
        englishButton = QRadioButton("English")
        englishButton.clicked.connect(lambda: setLanguageIndex(0))
        germanButton = QRadioButton("Deutsch")
        germanButton.clicked.connect(lambda: setLanguageIndex(1))

        languageLayout.addWidget(languageLabel)
        languageLayout.addWidget(englishButton)
        languageLayout.addWidget(germanButton)

        global languageIndex
        if languageIndex == 0:
            englishButton.setChecked(True)
        else:
            germanButton.setChecked(True)

        vertLayout.addWidget(backgroundColorBtn)
        vertLayout.addWidget(lineColorBtn)
        vertLayout.addLayout(languageLayout)

    def setColor(self, name):
        temp = QColorDialog.getColor()
        self.settings.setValue(name, temp.name())
        self.settings.sync()

    def changePort(self, newPort):
        ReadImage.port = newPort
        self.settings.setValue("Port", newPort)
        self.settings.sync()

    # Stolen from stackoverflow: https://stackoverflow.com/a/14224477
    # Returns a list of all the available port names
    def getAvailablePorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
