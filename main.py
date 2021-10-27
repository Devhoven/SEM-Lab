import os
import sys
import csv
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# Sets the style of pyqt
sys.argv += ['--style', 'Fusion']

# The GUI is natively written for a 1920x1080 Display
# If you set this scaling Factor to another value than one you can scale it to the target display size
scalingFactor = 2

# dir saves the path to the current project location
dir = os.path.dirname(__file__)

# Creating the dictionary based on the cvs file
reader = csv.reader(open(os.path.join(dir, 'assets', 'Translations.csv'), 'r', encoding='utf-8'), delimiter=';')
# The final dictionary
translations = dict()
for row in reader:
    # The Key is the term which is used to reference it in Code
    # The Value are the translations in the order of the file
    translations[row[0]] = row[1:]

settings = QSettings("REM", "REM GUI")

# Either sets the languageIndex to the one the user set, or 0 by default
languageIndex = settings.value("languageIndex", 0)

# Returns a string in the currently set Language from the key value "name"
def translate(name):
    global translations, languageIndex
    return translations[name][languageIndex]

# Sets and saves the new language index
def setLanguageIndex(newIndex):
    global languageIndex, settings
    languageIndex = newIndex
    settings.setValue("languageIndex", languageIndex)
    settings.sync()

if __name__ == "__main__":
    import App as a

    # Starts the application
    app = QApplication(sys.argv)
    ex = a.App(settings)
    app.setWindowIcon(QIcon("assets/Icon.png"))
    sys.exit(app.exec_())
