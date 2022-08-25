"""
Author: Michael Horina
This is the module that analyzes data about each line extracted via Tesseract
and attempts to categorize it in a way that makes lines filterable such that
records can be extracted easier without extra bloat from irrelevant text.
TODO: getfontsize

"""

from imagehandler import preprocess
import cv2
import numpy

def getcharacters(line: list) -> list:
    """
    This function returns a list of contours in a given image

    Parameters
    line : str
        The line to be split into characters

    Returns
    contours : list
        A list of all shapes found in the image with reduntant points removed.
    """
    contours, hierarchy = cv2.findContours(line, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def getfontsize(line : list, bestfit : bool = False) -> int:
    """
    This function takes a line image and calculates the approximate font height in pixels

    Parameters
    line : str
        The line to be calculated as a path
    bestfit : bool
        Whether to find the height of best fit for a line (for when lines may be skewed)
        note this increases processing time drastically

    Returns
    pix : int
        The height value as an integer in pixels.
    """
    
    if bestfit is True:
        shapes = getcharacters(line)
        blob = []
        for i in range(0, len(shapes)): #access each array
            for j in range(0, len(shapes[i])): #access each set within the array
                for k in range(0, len(shapes[i][j])): #access each set of points
                    blob.append(shapes[i][j])

        blob = numpy.array(blob, dtype=numpy.int32)
        newbox = cv2.minAreaRect(blob)
        if newbox[2] > 45:
            pix = newbox[1][0]/2
        else:
            pix = newbox[1][1]/2 #divided by 2 because the preprocessing upscales images 2x.
        return pix
    else:
        pix = len(line)/2 #divided by 2 because the preprocessing upscales images 2x.
    return pix

def characterizelines(lines : list) -> str:
    """
    This function takes a line image and calculates the approximate font height in pixels

    Parameters
    line : str
        The line to be calculated as a path
    bestfit : bool
        Whether to find the height of best fit for a line (for when lines may be skewed)
        note this increases processing time drastically

    Returns
    pix : int
        The height value as an integer in pixels.
    """