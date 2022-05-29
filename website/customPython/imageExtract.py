"""
Image_extract
Extracts all images from a pdf and applies appropriate soft masks to them if needed
Usage: from image_extract import image_extraction
Parameter: url of pdf
Author: Michael Horina
"""

import os
import fitz

def recoverpix(doc, x, imgdict):
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

def image_extraction(pdf):

    print(fitz.__doc__)
    if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
        raise SystemExit("require PyMuPDF v1.18.18+")

    fpref = "img"
    doc = fitz.open(pdf)
    print(doc.metadata)

    imagedir = os.path.join(os.path.dirname(pdf), os.path.splitext(os.path.basename(pdf))[0])
    if not os.path.exists(imagedir):
        os.makedirs(imagedir, exist_ok = True)
    
    lenXREF = doc.xref_length()
    print("XRef length: " + str(lenXREF))

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
            imgdict = recoverpix(doc, xref, imgdict) #create pix with mask
            if imgdict is None: #Ignore errors
                continue
            ext = "png"
            imgdata = imgdict["image"]

        imgn1 = fpref + "-%i.%s" % (xref, ext)
        imgname = os.path.join(imagedir, imgn1)
        ofile = open(imgname, "wb")
        ofile.write(imgdata)
        ofile.close()
    
    if len(smasks) > 0:
        imgdir_ls = os.listdir(imagedir)
        for smask in smasks:
            imgn1 = fpref + "-%i" % smask
            for f in imgdir_ls:
                if f.startswith(imgn1):
                    imgname = os.path.join(imagedir, f)
                    os.remove(imgname)