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

def generatelines(doc: str, page : int, fpref : str = "page") -> int:
    """
    Creates an image of each line of text from a source image

    Parameters
    doc : str
        Specify the document location for where images will be saved
    fpref : str
        The prefix of the filename to access page image from
        default = "page"
    page : str
        Specifies the current page lines are being split from for saving
        in a subdirectory
    Returns
    lines : int
        The number of lines extracted from an image
    """

    path = os.path.join(os.path.dirname(doc), os.path.splitext(os.path.basename(doc))[0])
    img = cv2.imread(os.path.join(path, fpref + str(page) + ".png"))
    path = os.path.join(path, fpref + str(page) + "/")
    if not os.path.exists(path): #Create the output folder if doesn't exist
        os.makedirs(path, exist_ok = True)
    data = pytesseract.image_to_data(img, config='--psm 1 --oem 1', lang="eng+ell", output_type=Output.DICT)
    
    countlines = 0
    for i in range(len(data['level'])):
        if data['level'][i] != 4:
            continue
        countlines = countlines + 1
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.imwrite(os.path.join(path, "line" + str(countlines) + ".png"), img[y:y+h, x:x+w])

def generateparagraphs(data: Output.DICT) -> int:
    countparagraphs = 0
    for i in range(len(data['level'])):
        if data['level'][i] != 3:
            continue
        countparagraphs = countparagraphs + 1
    return countparagraphs

def generateblocks(data: Output.DICT) -> int:
    countblocks = 0
    for i in range(len(data['level'])):
        if data['level'][i] != 2:
            continue
            countblocks = countblocks + 1
    return countblocks
