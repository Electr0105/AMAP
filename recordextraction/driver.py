from pdfhandler import *
from textextractor import *
import os
from imagehandler import preprocess
from textprocessing import *


pdf = "/mnt/e/2022 Industry Project/Resources/RVPfixed.pdf"


def processpdf(pdf : str):
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
    datafile = os.path.join(folder, os.path.splitext(os.path.basename(pdf))[0], ".dat")

    extractpages(pdf)

    pdfdata = {'level' : [], 'page_num' : [], 'block_num' : [], 'par_num' : [], 'line_num' : [], 'word_num' : [], 'left' : [], 'top' : [], 'width' : [], 'height' : [], 'conf' : [], 'text' : []}

    fout = open(datafile, "wb")
    pageno = 0
    for page in os.listdir(filefolder):
        abspath = os.path.join(filefolder, page)
        pagefile = cv2.imread(abspath)
        pagedata = getocrdata(pagefile)
        for i in range(len(pagedata['page_num'])):
            pagedata['page_num'][i] = pageno
        for key in pdfdata:
            pdfdata[key].append(pagedata[key])
        
        generatelines(os.path.join(filefolder, page))

processpdf(pdf)