"""
The main driver of the OCR process
Input parameters should be a single PDF file, start page and end page.
TODO: Create function to open PDF and split pages at user specified locations and:
- apply OCR to each page file, outputting data as a .txt file
- apply record identification and split + DB loading for each .txt file
- mark archive status as complete in DB
"""

from recordextraction.pdfhandler import extractpages
from recordextraction.textextractor import *
import os
from recordextraction.imagehandler import preprocess
from recordextraction.textprocessing import *
import sqlite3

sql3 = '/home/mike/AMAP/db.sqlite3'


def dbconnect(db : str) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    return conn

# def processpdf(pdf : str, db : sqlite3.Connection):
    """
    This function applies all the processing to a pdf in the necessary order

    Parameters
    pdf : str
        The pdf to be processed as an absolute path

    Returns
    """
    cur = db.cursor()
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
            if pagedata['level'][i] == 4:
                sqlstatement = "INSERT INTO Line("
        # db.execute(sqlstatement)
        generateimages(os.path.join(filefolder, page), pagedata)

