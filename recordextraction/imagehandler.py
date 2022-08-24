"""
Author: Michael Horina
This is the module that handles image functions: methods for preprocessing
images to increase accuracy of tesseract. Performing dilation/erosion and 
median blur to reduce noise helps greatly. 
TODO: fix preprocess

"""

import cv2

def preprocess(image : list) -> list:
    # Apply processing here
    rows = len(image)
    cols = len(image[0])

    erodekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    retval, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) #thresholding to eliminate light blemishes
    img = cv2.pyrUp(img, dstsize=(2 * cols, 2 * rows)) #scaled up
    for i in range(5):
        img = cv2.medianBlur(img, 3)
    img = cv2.dilate(img, erodekernel, iterations=1) #dilate
    retval, img = cv2.threshold(img, 128, 255, cv2.THRESH_OTSU)
    return img