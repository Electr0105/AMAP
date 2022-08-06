"""
Author: Michael Horina
This is the module that handles opening and extracting data from PDF
It will also generate a hash to ensure PDF upload with no errors

"""
import hashlib
import fitz
import os

BUFSIZE = 65536

#open pdf and generate hash
def generatehash(pdf: str) -> str:
    """
    This function takes a pdf as a path and returns MD5 and SHA1 hashes of the file.

    Parameters
    pdf : str
        The pdf to be hashed as a path

    Returns
    md5hash : str
        A MD5 hash of the file
    sha1hash : str
        A SHA1 hash of the file
    """
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(pdf, 'rb') as f:
        while True:
            data = f.read(BUFSIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    md5hash = "MD5: {0}".format(md5.hexdigest())
    sha1hash = "SHA1: {0}".format(sha1.hexdigest())
    return md5hash, sha1hash

def extracttext(pdf: str, writetofile: str = None) -> str:
    """
    This function extracts all text contained within the PDF file

    Parameters
    pdf : str
        The pdf to be hashed as a path
    writetofile : str
        Specify a text file to write text to. If set to None will return text in memory - NOT RECOMMENDED
        default = None

    Returns
    text : str
        The text contained within the PDF. If writetofile is specified returns the file.
    """
    doc = fitz.open(pdf)
    if writetofile is None:
        text = ''""''
        for page in doc:
            text += str(page.get_text())
        return text
        
    else:
        fout = open(writetofile, 'wb')
        for page in doc:
            fout.write(page.get_text().encode('utf-8') + bytes((12,)))
        fout.close()
        return writetofile

def extractimages(pdf: str, prefix: str = "page", saveto: str = None) -> bool:
    """
    This function extracts all images contained within the PDF file

    Parameters
    pdf : str
        The pdf to be hashed as a path
    prefix : str
        Specify the names of the images extracted and saved to file.
        default = "page"
    saveto : str
        Specify a directory to save images to. If set to None will create a directory at
        the location of the PDF with the name of the PDF, else creates a directory at PDF
        location with name saveto
        default = None

    Returns
    result : bool
        Returns True if operation successful
    """
    print(fitz.__doc__)
    if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
        raise SystemExit("require PyMuPDF v1.18.18+")

    if prefix is None:
        prefix = "page"
    doc = fitz.open(pdf)
    print(doc.metadata)

    if saveto is None:
        saveto = os.path.join(os.path.dirname(pdf), os.path.splitext(os.path.basename(pdf))[0])
    else:
        saveto = os.path.join(os.path.dirname(pdf), saveto)
    if not os.path.exists(saveto): #Create the output folder if doesn't exist
        os.makedirs(saveto, exist_ok = True)
    
    lenXREF = doc.xref_length()
    print("XRef length: " + str(lenXREF))

    imgcnt = 0

    smasks = set()

    for xref in range(1, lenXREF):

        pdfobject = doc.xref_get_key(xref, "Subtype")
        if doc.xref_get_key(xref, "Subtype")[1] != "/Image":
            continue #ignore non-image objects
    
        imgdict = doc.extract_image(xref)

        if not imgdict: #not an image
            continue
        if xref in smasks: #ignore smask
            continue

        smask = imgdict["smask"]
        if smask > 0: #store /SMask xref
            smasks.add(smask)

        imgdata = imgdict["image"]
        ext = imgdict["ext"]

        if smask > 0:
            imgdict = recoverpix(doc, imgdict) #create pix with mask
            if imgdict is None: #Ignore errors
                continue
            ext = "png"
            imgdata = imgdict["image"]

        imgcnt += 1

        imgn1 = prefix + "-%i.%s" % (imgcnt, ext)
        imgname = os.path.join(saveto, imgn1)
        ofile = open(imgname, "wb")
        ofile.write(imgdata)
        ofile.close()
    
    if len(smasks) > 0:
        imgdir_ls = os.listdir(saveto)
        for smask in smasks:
            imgn1 = prefix + "-%i" % smask
            for f in imgdir_ls:
                if f.startswith(imgn1):
                    imgname = os.path.join(saveto, f)
                    os.remove(imgname)

    return True

#This is a method to be used internally by image extraction
#It applies soft masks to images, adding alpha channels if needed
#and preventing weird black artifacting.
def recoverpix(doc, imgdict):
    """Return pixmap for item with an image mask."""
    s = imgdict["smask"]  # xref of its image mask

    try:
        pix0 = fitz.Pixmap(imgdict["image"])
        mask = fitz.Pixmap(doc.extract_image(s)["image"])
        pix = fitz.Pixmap(pix0, mask)
        if pix0.n > 3:
            ext = "pam"
        else:
            ext = "png"
        return {"ext": ext, "colorspace": pix.colorspace.n, "image": pix.tobytes(ext)}
    except:
        return None

def extractpages(pdf: str, saveto: str = None):
    """
    Parameters

    pdf : str
        Specify the pdf to be converted to images as full or relative path in string form.
    saveto : str
        Specify the directory to save page images to.
        default = file location as <filename>-pages/

    Returns
    pages : int
        Returns the number of pages converted to image
    """


    print(fitz.__doc__)
    if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
        raise SystemExit("require PyMuPDF v1.18.18+")

    doc = fitz.open(pdf)
    # print(doc.metadata)

    if saveto is None:
        saveto = os.path.join(os.path.dirname(pdf), os.path.splitext(os.path.basename(pdf))[0])
    else:
        saveto = os.path.join(os.path.dirname(pdf), saveto)
    if not os.path.exists(saveto): #Create the output folder if doesn't exist
        os.makedirs(saveto, exist_ok = True)
    
    page_count = doc.page_count
    print("Number of pages: " + str(page_count))

    for pageno in range(page_count):
        page = doc.load_page(pageno)
        image = page.get_pixmap(dpi=300, alpha=False)
        imgdata = image.tobytes("png")
        imgfile = os.path.join(saveto, "page" + str(pageno) + ".png")
        fout = open(imgfile, "wb")
        fout.write(imgdata)
        fout.close()

    return page_count