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

def getocrdata(image : list, output_type : str = 'd') -> dict:
    """
    Runs tesseract on the specified image

    Parameters
    image : list
        the specified image as an array
    output_type : str
        whether the output is a line by line string ('s') or default case - a dict of arrays ('d')
    Returns
    data : dict
        a string containing all the text found by tesseract
    """
    if output_type.lower() == 's':
        output = Output.STRING
    elif output_type.lower() == 'd':
        output = Output.DICT
    else:
        return "Error: unknown output entered"
    image = preprocess(image)
    data = pytesseract.image_to_data(image, config='--psm 1 --oem 1', lang="trendall", output_type=output)      
    return data

def generateimages(page : str, data : str, overwrite : bool = False) -> int:
    """
    Creates an image of each line of text from a source image

    Parameters
    page : str
        Specifies the current page lines are being split from for saving
        in a subdirectory
    overwrite : bool
        default = False
        If set to true will re-process lines, otherwise if line file exists will skip.

    Returns
    lines : int
        The number of lines extracted from an image
    """

    pagefolder = os.path.dirname(page)
    pagename = os.path.basename(page)
    filefolder = os.path.join(pagefolder, os.path.splitext(pagename)[0])
    image = cv2.imread(page)
    image = preprocess(image)

    if not os.path.exists(filefolder): #Create the output folder if doesn't exist
        os.makedirs(filefolder, exist_ok = True)
    
    countlines = 0
    countwords = 0
    for i in range(len(data['level'])):
        if data['level'][i] == 4:
            countlines += 1
            if overwrite == False:
                if os.path.exists(os.path.join(filefolder, "line" + str(countlines) + ".png")):
                    continue    
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            cv2.imwrite(os.path.join(filefolder, "line" + str(countlines) + ".png"), image[y:y+h, x:x+w])
            countwords = 0 # When a line is extracted the word count is reset for the word extraction that follows
        if data['level'][i] == 5:
            countwords += 1
            if overwrite == False:
                if os.path.exists(os.path.join(filefolder, "line" + str(countlines), "word" + str(countwords) + ".png")):
                    continue
            linefolder = os.path.join(filefolder, "line" + str(countlines))
            if not os.path.exists(linefolder):
                os.makedirs(linefolder, exist_ok = True)
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            cv2.imwrite(os.path.join(linefolder, "word" + str(countwords) + ".png"), image[y:y+h, x:x+w])
        else:
            continue
    return countlines, countwords