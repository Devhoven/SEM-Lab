import cv2
import time
import serial
from main import *
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def setPercentage(newPercentage):
    global percentage
    percentage = newPercentage


def getImage(updateInfoSignal):
    try:
        remData = readImageFromREM(updateInfoSignal)
    except serial.SerialTimeoutException:
        updateInfoSignal.emit("SerialTimeoutException")
        return False, None
    except serial.SerialException:
        updateInfoSignal.emit("SerialException")
        return False, None

    return True, readImageFromList(updateInfoSignal, remData)


def readImageFromREM(updateInfoSignal):
    global percentage
    # Timeout has to be set to zero, otherwise the processing won't work
    ser = serial.Serial(port, baudrate, timeout=0)

    sr = bytearray()
    lst = []

    wasNotZero = False

    while not wasNotZero or percentage != 0:
        sr.extend(ser.read(bytelength))

        if len(sr) >= 200:

            updateInfoSignal.emit(translate("ReceiveDataInfo").format(percentage))
            wasNotZero = percentage > 0 or wasNotZero

            lst.append(sr[:200])
            sr = sr[200:len(sr)]

    ser.close()
    return lst


# reading bytestrings line per from buffer txt file
def readImageFromList(updateInfoSignal, lst, steps=20):
    progression, written = 0, 0  # progression in percent, written pixels
    updateInfoSignal.emit(translate("ProcessingDataInfo").format(progression))
    image = np.zeros((size, size)).astype(np.int8)  # initializing image as 2d array of type int8
    divider = int(size ** 2 / steps)  # divider to calculate progression bar from written pixels
    step = int(100 / steps)  # steps to count on progression
    index = 0
    sr = bytearray()

    while index < len(lst):

        sr.extend(lst[index])
        while len(sr) >= 5:
            # checking for expected sequence of a pixel data package: 00000dd1 ddddddv0 vvvvvvv0 vvvhhhh0 hhhhhh0h
            if (sr[0] & 1, sr[1] & 1, sr[2] & 1, sr[3] & 1, sr[4] & 1) == (1, 0, 0, 0, 0):
                # if sequence match, extracting position and brightness from pixel data package
                horizontal, vertikal, pixel = getPixelData(sr, -47, 0)

                # writes extracted pixel brightness into corresponding vector of 2d image array
                image[vertikal][horizontal] = pixel

                written += 1  # counting up written pixel
                if written % divider == 0:  # If divider is an integer multiple of written
                    updateInfoSignal.emit(translate("ProcessingDataInfo").format(progression))
                    progression += step  # counting up progression by step

                sr = sr[5:len(sr)]  # extracting first 5 bytes from sr bytearray buffer
            else:
                sr = sr[1:len(sr)]  # if sequence doesn't match, extracting first byte in sr bytearray buffer

        index += 1

    updateInfoSignal.emit("1")
    # Those are needed to make it a 3 channel image
    image = np.float32(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = image.astype(np.uint8)
    return image  # returning 2d image


# bitstream format in 5 bytes: 00000DD1 DDDDDDV0 VVVVVVV0 VVVHHHH0 HHHHHHH0
# uses bitshifting and addition to extract data from bytestring
# uses arithmetic overflow with rest modulo operation to shift vertical and or horizontal index
def getPixelData(d, h_shift, v_shift):
    p = ((d[0] >> 1) << 6) + (d[1] >> 2)
    h = (((d[3] & 30) << 6) + (d[4] >> 1) + h_shift) % size
    v = (((d[1] & 2) << 9) + ((d[2] >> 1) << 3) + (d[3] >> 5) + v_shift) % size
    return h, v, p


port = settings.value("Port", "")
size = 2048
percentage = 0
baudrate = 11000000
bytelength = 10000
f1w, f2h, f2w, f2b = 200, 500, 500, 10
displayFrame = f2w - f2b
