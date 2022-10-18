from pdfhandler import extractpages
from textextractor import *
import os
from imagehandler import preprocess
from textprocessing import *
import sqlite3

sql3 = '/home/mike/AMAP/db.sqlite3'

pdf = "/mnt/e/2022 Industry Project/Resources/RVPfixed.pdf"

def dbconnect(db : str) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    return conn

# def initialize(db : sqlite3.connection):
#     sql

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


tessdata = getocrdata(cv2.imread("/mnt/e/2022 Industry Project/Resources/RVPfixed/page56.png", cv2.IMREAD_COLOR), output_type='s')

file = "/mnt/e/2022 Industry Project/Resources/page56.txt"
fout = open(file, 'w')
fout.write(tessdata)