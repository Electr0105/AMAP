from pdfhandler import *
from textextractor import *
import os
from imagehandler import preprocess
from textprocessing import *
import sqlite3
import cv2

sql3 = '/home/mike/AMAP/db.sqlite3'

pdf = "/mnt/e/2022 Industry Project/Resources/RVPfixed.pdf"

def dbconnect(db : str) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    return conn

# def initialize(db : sqlite3.connection):
#     sql

def processpdf(pdf : str, db : sqlite3.Connection):
    """
    This function applies all the processing to a pdf in the necessary order

    Parameters
    pdf : str
        The pdf to be processed as an absolute path

    Returns
    """

    folder = os.path.dirname(pdf)
    filename = os.path.basename(pdf)
    filefolder = os.path.join(folder, os.path.splitext(filename)[0])
    lines = os.path.join(filefolder, "lines")
    if not os.path.exists(lines):
        os.makedirs(lines, exist_ok=True)

    extractpages(pdf)

    pageno = 0
    for page in os.listdir(filefolder):
        abspath = os.path.join(filefolder, page)
        pagefile = cv2.imread(abspath)
        pagedata = getocrdata(pagefile)
        for i in range(len(pagedata['page_num'])):
            pagedata['page_num'][i] = pageno
            # if pagedata['level'][i] == 
        # sqlstatement = "INSERT INTO Page "
        # db.execute(sqlstatement)
        generateimages(os.path.join(filefolder, page), pagedata)


# processpdf(pdf, dbconnect(sql3))
# linenumber = 0
# image = "/mnt/e/2022 Industry Project/Resources/RVPfixed/page"

# image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
# bordered = cv2.copyMakeBorder(image, 4, 4, 4, 4, cv2.BORDER_CONSTANT, None, 255)
# bordered = cv2.copyMakeBorder(bordered, 2, 2, 2, 2, cv2.BORDER_CONSTANT, None, 0)
# cv2.imwrite("/mnt/e/2022 Industry Project/Resources/data/")
