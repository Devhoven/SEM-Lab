import os
import sys
import csv
import ctypes
import locale
from MainWindow import *
from PyQt5.QtWidgets import *


# dir saves the path to the current project location
dir = os.path.dirname(__file__)

windll = ctypes.windll.kernel32
language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

languageIndex = 0

# If the system language is set to german, it sets the language to german, otherwise it's english
if "de" in language:
    languageIndex = 1

# Creating the dictionary based on the cvs file
reader = csv.reader(open(os.path.join(dir, 'assets', 'Translations.csv'), 'r', encoding='utf-8'), delimiter=';')
# The final dictionary
translations = dict()
for row in reader:
    # The Key is the term which is used to reference it in Code
    # The Value are the translations in the order of the file
    translations[row[0]] = row[1:]

# Returns a string in the currently set Language from the key value "name"
def translate(name):
    global translations, languageIndex
    return translations[name][languageIndex]

if __name__ == "__main__":
    sys.argv += ['--style', 'Fusion']

    from MainWindow import *

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
