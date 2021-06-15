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


class SpotSizeWidget(MetadataWidget):

    def __init__(self, parent):
        super().__init__(parent, "SpotSize")

        spotSizeWidget = QWidget(parent)
        spotSizeWidget.setStyleSheet("border: 0;")
        self.spotSizeBtnGroup = QButtonGroup(spotSizeWidget)
        spotSizeLayout = QHBoxLayout(spotSizeWidget)

        self.spotSizeLargeBtn = QRadioButton("Large")
        spotSizeLayout.addWidget(self.spotSizeLargeBtn)
        self.spotSizeBtnGroup.addButton(self.spotSizeLargeBtn)
        self.spotSizeMedBtn = QRadioButton("Medium")
        spotSizeLayout.addWidget(self.spotSizeMedBtn)
        self.spotSizeBtnGroup.addButton(self.spotSizeMedBtn)
        self.spotSizeSmallBtn = QRadioButton("Small")
        spotSizeLayout.addWidget(self.spotSizeSmallBtn)
        self.spotSizeBtnGroup.addButton(self.spotSizeSmallBtn)

        self.layout.addWidget(spotSizeWidget)

    def getValue(self):
        if self.spotSizeLargeBtn.isChecked():
            return "0"
        elif self.spotSizeMedBtn.isChecked():
            return "1"
        elif self.spotSizeSmallBtn.isChecked():
            return "2"
        return "-1"

    def setValue(self, value):
        if value == "0":
            self.spotSizeLargeBtn.setChecked(True)
        elif value == "1":
            self.spotSizeMedBtn.setChecked(True)
        elif value == "2":
            self.spotSizeSmallBtn.setChecked(True)

    def reset(self):
        self.spotSizeBtnGroup.setExclusive(False)
        self.spotSizeLargeBtn.setChecked(False)
        self.spotSizeMedBtn.setChecked(False)
        self.spotSizeSmallBtn.setChecked(False)
        self.spotSizeBtnGroup.setExclusive(True)


class CoarseWidget(MetadataWidget):

    def __init__(self, parent):
        super(CoarseWidget, self).__init__(parent, "Coarse")

        self.valueChanged = False

        self.coarseSlider = QSlider(Qt.Horizontal)
        self.coarseSlider.setMinimum(1)
        self.coarseSlider.setMaximum(16)
        self.coarseSlider.valueChanged.connect(self.valueChange)
        self.coarseSlider.setTickPosition(QSlider.TicksBelow)
        self.layout.addWidget(self.coarseSlider)

        coarseLayout = QHBoxLayout()

        minLabel = QLabel("1")
        coarseLayout.addWidget(minLabel)
        maxLabel = QLabel("16")
        coarseLayout.addWidget(maxLabel)
        coarseLayout.setAlignment(maxLabel, Qt.AlignRight)

        self.layout.addLayout(coarseLayout)

    def valueChange(self):
        self.valueChanged = True
        self.label.setText("Coarse" + " (" + str(self.coarseSlider.value()) + ")")

    def setValue(self, value):
        if value == "-1":
            self.coarseSlider.setValue(1)
            self.valueChanged = False
            self.label.setText("Coarse")
            return

        self.coarseSlider.setValue(int(value))

    def getValue(self):
        if self.valueChanged:
            return self.coarseSlider.value()
        return -1;


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
