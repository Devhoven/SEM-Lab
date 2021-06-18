from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MetadataWidget(QWidget):

    def __init__(self, parent, name):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.font = QFont()
        self.font.setPointSize(12)

        self.label = QLabel(name)
        self.label.setFont(self.font)
        self.layout.addWidget(self.label)

    def getValue(self):
        return -1

    def setValue(self, value):
        pass

    def reset(self):
        pass


class CoarseWidget(MetadataWidget):

    def __init__(self, parent):
        super().__init__(parent, "Coarse")

        coarseWidget = QWidget(parent)
        coarseWidget.setStyleSheet("border: 0;")
        self.coarseBtnGroup = QButtonGroup(coarseWidget)
        coarseLayout = QHBoxLayout(coarseWidget)

        self.coarseLargeBtn = QRadioButton("Large")
        coarseLayout.addWidget(self.coarseLargeBtn)
        self.coarseBtnGroup.addButton(self.coarseLargeBtn)
        self.coarseMedBtn = QRadioButton("Medium")
        coarseLayout.addWidget(self.coarseMedBtn)
        self.coarseBtnGroup.addButton(self.coarseMedBtn)
        self.coarseSmallBtn = QRadioButton("Small")
        coarseLayout.addWidget(self.coarseSmallBtn)
        self.coarseBtnGroup.addButton(self.coarseSmallBtn)

        self.layout.addWidget(coarseWidget)

    def getValue(self):
        if self.coarseLargeBtn.isChecked():
            return "0"
        elif self.coarseMedBtn.isChecked():
            return "1"
        elif self.coarseSmallBtn.isChecked():
            return "2"
        return "-1"

    def setValue(self, value):
        if value == "0":
            self.coarseLargeBtn.setChecked(True)
        elif value == "1":
            self.coarseMedBtn.setChecked(True)
        elif value == "2":
            self.coarseSmallBtn.setChecked(True)

    def reset(self):
        self.coarseBtnGroup.setExclusive(False)
        self.coarseLargeBtn.setChecked(False)
        self.coarseMedBtn.setChecked(False)
        self.coarseSmallBtn.setChecked(False)
        self.coarseBtnGroup.setExclusive(True)


class SpotSizeWidget(MetadataWidget):

    def __init__(self, parent):
        super(SpotSizeWidget, self).__init__(parent, "SpotSize")

        self.valueChanged = False

        self.spotSizeSlider = QSlider(Qt.Horizontal)
        self.spotSizeSlider.setMinimum(1)
        self.spotSizeSlider.setMaximum(16)
        self.spotSizeSlider.valueChanged.connect(self.valueChange)
        self.spotSizeSlider.setTickPosition(QSlider.TicksBelow)
        self.layout.addWidget(self.spotSizeSlider)

        spotSizeLayout = QHBoxLayout()

        minLabel = QLabel("1")
        spotSizeLayout.addWidget(minLabel)
        maxLabel = QLabel("16")
        spotSizeLayout.addWidget(maxLabel)
        spotSizeLayout.setAlignment(maxLabel, Qt.AlignRight)

        self.layout.addLayout(spotSizeLayout)

    def valueChange(self):
        self.valueChanged = True
        self.label.setText("SpotSize" + " (" + str(self.spotSizeSlider.value()) + ")")

    def setValue(self, value):
        if value == "-1":
            self.spotSizeSlider.setValue(1)
            self.valueChanged = False
            self.label.setText("SpotSize")
            return

        self.spotSizeSlider.setValue(int(value))

    def getValue(self):
        if self.valueChanged:
            return self.spotSizeSlider.value()
        return -1


class CurrentWidget(MetadataWidget):

    def __init__(self, parent):
        super().__init__(parent, "Current")

        self.currentLineEdit = QLineEdit(parent)
        self.currentLineEdit.setValidator(QIntValidator())
        self.layout.addWidget(self.currentLineEdit)

    def setValue(self, value):
        self.currentLineEdit.setText(value)

    def getValue(self):
        return self.currentLineEdit.text()


class VoltageWidget(MetadataWidget):

    def __init__(self, parent):
        super().__init__(parent, "Voltage")

        voltageWidget = QWidget(parent)
        voltageWidget.setStyleSheet("border: 0;")
        self.voltageBtnGroup = QButtonGroup(voltageWidget)
        voltageLayout = QHBoxLayout(voltageWidget)

        self.voltagePlusBtn = QRadioButton("SE(+)")
        voltageLayout.addWidget(self.voltagePlusBtn)
        self.voltageBtnGroup.addButton(self.voltagePlusBtn)
        self.voltageMinusBtn = QRadioButton("BSE(-)")
        voltageLayout.addWidget(self.voltageMinusBtn)
        self.voltageBtnGroup.addButton(self.voltageMinusBtn)

        self.layout.addWidget(voltageWidget)

    def reset(self):
        self.voltageBtnGroup.setExclusive(False)
        self.voltagePlusBtn.setChecked(False)
        self.voltageMinusBtn.setChecked(False)
        self.voltageBtnGroup.setExclusive(True)

    def getValue(self):
        if self.voltagePlusBtn.isChecked():
            return "0"
        elif self.voltageMinusBtn.isChecked():
            return "1"
        return "-1"

    def setValue(self, value):
        if value == "0":
            self.voltagePlusBtn.setChecked(True)
        elif value == "1":
            self.voltageMinusBtn.setChecked(True)


class FocusWidget(MetadataWidget):

    def __init__(self, parent):
        super().__init__(parent, "Focus")

        focusWidget = QWidget(parent)
        focusWidget.setStyleSheet("border: 0;")
        self.focusBtnGroup = QButtonGroup(focusWidget)
        focusLayout = QHBoxLayout(focusWidget)

        self.focusOffBtn = QRadioButton("OFF")
        focusLayout.addWidget(self.focusOffBtn)
        self.focusBtnGroup.addButton(self.focusOffBtn)
        self.focusOnBtn = QRadioButton("ON")
        focusLayout.addWidget(self.focusOnBtn)
        self.focusBtnGroup.addButton(self.focusOnBtn)

        self.layout.addWidget(focusWidget)

    def reset(self):
        self.focusBtnGroup.setExclusive(False)
        self.focusOffBtn.setChecked(False)
        self.focusOnBtn.setChecked(False)
        self.focusBtnGroup.setExclusive(True)

    def getValue(self):
        if self.focusOffBtn.isChecked():
            return "0"
        elif self.focusOnBtn.isChecked():
            return "1"
        return "-1"

    def setValue(self, value):
        if value == "0":
            self.focusOffBtn.setChecked(True)
        elif value == "1":
            self.focusOnBtn.setChecked(True)
