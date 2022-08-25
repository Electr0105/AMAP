"""
Author: Michael Horina
This is the module that handles text functions: tesseract calls for OCR, 
cropping tesseract results down into text blocks and matching document images.
"""

import os
import cv2
import pytesseract
from pytesseract import Output
from imagehandler import preprocess
from pdfhandler import *

def runtesseract(image: list, type: str = "text") -> str:
    """
    Runs tesseract on the specified image and return text

    Parameters
    image : list
        the specified image run OCR on
    type : str
        default = "text"
        "text" returns contents while "data" returns OCR data
    Returns
    text: str
        a string containing all the text found by tesseract
    """

    if type == "text":
        text = str(pytesseract.image_to_string(image, config='--psm 1 --oem 1', lang="eng+ell"))
    if type == "data":
        text = str(pytesseract.image_to_data(image, config='--psm 1 --oem 1', lang="eng+ell"))
    return text

def getocrdata(image:list) -> dict:
    """
    Runs tesseract on the specified image

    Parameters
    image: str
        the specified image to open and run OCR on
    Returns
    data: dict
        a string containing all the text found by tesseract
    """

    img = preprocess(image)
    data = pytesseract.image_to_data(img, config='--psm 1 --oem 1', lang="eng+ell", output_type=Output.DICT)
    return data

def generatelines(page : str, overwrite : bool = False) -> int:
    """
    Creates an image of each line of text from a source image

    Parameters
    page : str
        Specifies the current page lines are being split from for saving
        in a subdirectory
    overwrite : bool
        If set to true will re-process lines, otherwise if line file exists will skip.

    Returns
    lines : int
        The number of lines extracted from an image
    """

    folder = os.path.dirname(page)
    filename = os.path.basename(page)
    filefolder = os.path.join(folder, os.path.splitext(filename)[0])
    image = cv2.imread(page)

    if not os.path.exists(filefolder): #Create the output folder if doesn't exist
        os.makedirs(filefolder, exist_ok = True)
    data = pytesseract.image_to_data(page, config='--psm 1 --oem 1', lang="eng+ell", output_type=Output.DICT)
    
    countlines = 0
    for i in range(len(data['level'])):
        if data['level'][i] != 4:
            continue
        countlines = countlines + 1
        if overwrite == False:
            if os.path.exists(os.path.join(filefolder, "line" + str(countlines) + ".png")):
                continue
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.imwrite(os.path.join(filefolder, "line" + str(countlines) + ".png"), image[y:y+h, x:x+w])

    return countlines