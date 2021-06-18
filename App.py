import os
import subprocess
from main import *
import numpy as np
from Widgets.SettingsDialog import *
from Widgets.Modes.FullPhotoMode import *
from Widgets.UiContainer import UiContainer


# The main class, which contains every top level class
class App(QMainWindow):

    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.bar = None
        self.setupMenuBar()

        # mainWidgetCon is the central widget which swaps between the normal GUI and the mode where you are only able to
        # see current image
        self.mainWidgetCon = QStackedWidget(self)
        self.uiContainer = UiContainer(self, settings)
        self.fullPhotoMode = FullPhotoMode(self)
        self.mainWidgetCon.addWidget(self.uiContainer)
        self.mainWidgetCon.addWidget(self.fullPhotoMode)
        self.setCentralWidget(self.mainWidgetCon)

        self.setWindowTitle(translate("Title"))
        self.settingsDialog = SettingsDialog(self, settings)

        self.viewMenu = None

        self.setStyle()

        self.fullscreen = False

        self.showMaximized()

    def setupMenuBar(self):
        self.bar = self.menuBar()
        self.programMenu = self.bar.addMenu(translate("ProgramBarName"))
        self.viewMenu = self.bar.addMenu(translate("ViewBarName"))
        self.helpMenu = self.bar.addMenu(translate("HelpBarName"))

        self.addAction(self.programMenu, translate("Settings"), "e", self.openSettings)
        self.addAction(self.programMenu, translate("Close"), "ESC", self.close)

        self.addAction(self.viewMenu, translate("FullScreen"), "F1", self.toggleWindowState)
        self.addAction(self.viewMenu, translate("LiveMode"), "1", lambda: self.uiContainer.changeModeTo(0))
        self.addAction(self.viewMenu, translate("PhotoMode"), "2", lambda: self.uiContainer.changeModeTo(1))
        self.addAction(self.viewMenu, translate("FullScreenPhoto"), "a", self.toggleFullPhoto)

        self.addAction(self.helpMenu, "README", "r", self.openREADME)
        self.addAction(self.helpMenu, translate("Manual"), "m", self.openManual)
        self.addAction(self.helpMenu, translate("KeyboardImg"), "k", self.openKeyboardImg)

    # Just a small helper method which adds a action to the view menu
    def addAction(self, menu, name, shortcut, triggered):
        action = QAction(name, self)
        action.setShortcut(shortcut)
        action.triggered.connect(triggered)
        menu.addAction(action)

    # The general style of the application is set here
    # No color or borders etc. are set in other files
    def setStyle(self):
        backgroundColor = "#162936"
        fontColor = "#e6e6ea"
        borderColor = "black"

        switchBtnColor = "#e6e6ea"
        switchBtnDisabledColor = "#AAAAAA"
        switchBtnHoverColor = "#a6a6ea"
        switchBtnFontColor = "black"

        buttonBackgroundColor = "#291749"
        buttonHoverColor = "#291729"

        self.setStyleSheet("* { background-color: " + backgroundColor + "; color: " + fontColor + "; }"
                           ".QToolTip { color: " + fontColor + "; border: 2px solid " + borderColor + "; }"
                           ".QMainWindow { background-color: " + buttonBackgroundColor + "; }"
                                                                                         
                           ".QMenu { color: white; border: 1px solid " + borderColor + "; }"
                           ".QMenu { background-color: " + buttonBackgroundColor + "; }"
                           ".QMenu::item:selected { background-color: " + buttonHoverColor + "; }"
                                                                                       
                           ".QLabel { color: " + fontColor + "; }"
                           ".QWidget { background-color: " + backgroundColor + "; border: 2px solid " + borderColor + "; }"
                           ".QPushButton { background-color: " + buttonBackgroundColor + "; color: " + fontColor + "; }"
                           ".QPushButton:hover { background-color: " + buttonHoverColor + "; }"
                                                                                                                   
                           ".QPushButton#SwitchBtn { background-color: " + switchBtnColor + "; color: " + switchBtnFontColor + "; }"
                           ".QPushButton#SwitchBtn:hover { background-color: " + switchBtnHoverColor + "; }"
                           ".QPushButton#SwitchBtn:disabled { background-color: " + switchBtnDisabledColor + "; }"
                                                                                                                            
                           ".QComboBox { color: " + fontColor + "; background-color: " + buttonBackgroundColor + "; height: 20; margin-top: 5; padding: 5; }"
                           ".QComboBox QAbstractItemView { border: 1px solid " + borderColor + "; color: " + fontColor + "; }"
                           ".QComboBox:hover { border: 1px solid red; color: " + fontColor + "; }"
                                                                                       
                           ".QScrollArea { border: 1px solid " + borderColor + "; }"
                           ".QScrollArea .QWidget { border: 0; }")

        self.bar.setStyleSheet("color: white; border-bottom: 1px solid black;")

    # Gets called when a key is pressed
    # Only works reliable on the QMainWindow fsr
    def keyPressEvent(self, event):
        # 1677216 is the key code for Escape
        if event.key() == 16777216:
            # Checks if the fullPhotoMode is currently active or not
            if self.mainWidgetCon.currentIndex() == 0:
                # If not, the application gets closed
                self.close()
            else:
                # If that is the case, the main GUI gets the focus again
                self.toggleFullPhoto()
        # 65 is the key code for 'a' and it toggels between the fullPhotoMode and the normal GUI
        elif event.key() == 65:
            self.toggleFullPhoto()

    def toggleFullPhoto(self):
        if self.mainWidgetCon.currentIndex() == 0:
            self.showFullPhotoMode(self.uiContainer.photoMode.image)
        else:
            self.bar.setVisible(True)
            self.setStyle()
            self.mainWidgetCon.setCurrentIndex(0)
            self.setWindowState()

    # Hides the menu bar and sets the focus to the fullPhotoMode
    # It also updates the image
    def showFullPhotoMode(self, img):
        self.bar.setVisible(False)
        self.setStyleSheet("background-color: " + str(self.settings.value("PhotoBackgroundColor", "#DDDDDD")))
        self.fullPhotoMode.setImageNP(img)
        self.mainWidgetCon.setCurrentIndex(1)
        if not self.fullscreen:
            self.showFullScreen()

    # Toggles between the photoMode and liveMode
    def toggleMode(self):
        if self.uiContainer.modeCon.currentIndex() == 0:
            self.uiContainer.changeModeTo(1)
        else:
            self.uiContainer.changeModeTo(0)

    # Toggles between a maximized and a fullscreen window
    def toggleWindowState(self):
        self.fullscreen = not self.fullscreen
        self.setWindowState()

    # Sets the window state, depending on the self.fullscreen variable
    def setWindowState(self):
        if self.fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()

    # Opens the settings Dialog
    def openSettings(self):
        self.settingsDialog.exec()

    # Opens the manual in the default system viewer
    def openManual(self):
        global dir
        os.startfile(os.path.join(dir, 'assets', 'Manual.pdf'), "open")

    # Opens the manual in the default system viewer
    def openREADME(self):
        global dir
        os.startfile(os.path.join(dir, 'assets', 'Readme.pdf'), "open")

    # Opens the keyboard image in the fullPhotoMode
    def openKeyboardImg(self):
        global dir
        self.showFullPhotoMode(np.array(Image.open(os.path.join(dir, 'assets', 'Keyboard.jpg'))))

    # This event gets called when the window is closed, and is used to release all resources
    def closeEvent(self, event):
        self.uiContainer.close()
