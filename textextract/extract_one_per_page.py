"""
extract_one_per_page
Checks only one image exists per page and if so, extracts that image.
Performs slower than image_extract but images are in correct page order.
Author: Michael Horina
"""

import os;
import fitz;

def recoverpix(doc, item):
    """Return pixmap for item with an image mask."""
    xref = item[0]  # xref of PDF image
    smask = item[1] # xref of its /SMask

    # special case: /SMask or /Mask exists
    if smask > 0:
        pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
        mask = fitz.Pixmap(doc.extract_image(smask)["image"])
        pix = fitz.Pixmap(pix0, mask)
        if pix0.n > 3:
            ext = "pam"
        else:
            ext = "png"

        return { # create dictionary expected by caller
            "ext": ext,
            "colorspace": pix.coorspace.n,
            "image": pix.tobytes(ext),
        }
    
    # special case: /ColorSpace definition exists
    # covnert these cases to RGB PNG images
    if "/ColorSpace" in doc.xref_object(xref, compressed=True):
        pix = fitz.Pixmap(doc, xref)
        pix = fitz.Pixmap(fitz.csRGB, pix)
        return { # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": pix.tobytes("png"),
        }
    return doc.extract_image(xref) # otherwise return image as is

def image_extraction_by_page(pdf, imagedir=None, fpref="page"):
    """
    Parameters
    ----------
    pdf : str
        Specify the pdf to be converted to images as full or relative path in string form.

    imgdir : str, default=None
        Specify the output folder containing the images. Default is a new directory named '<pdfname>-pages'

    fpref : str, default=None
        Specify the prefix of the image files. Default is 'page'

    Returns
    -------
    Status as string
    """


    print(fitz.__doc__)
    if not tuple(map(int, fitz.version[0].split("."))) >= (1, 18, 18):
        raise SystemExit("require PyMuPDF v1.18.18+")

    if fpref is None:
        fpref = "page"
    doc = fitz.open(pdf)
    print(doc.metadata)

    if imagedir is None:
        imagedir = os.path.join(os.path.dirname(pdf), os.path.splitext(os.path.basename(pdf))[0]) + "pages"
    else:
        imagedir = os.path.join(os.path.dirname(pdf), imagedir)
    if not os.path.exists(imagedir): #Create the output folder if doesn't exist
        os.makedirs(imagedir, exist_ok = True)
    
    page_count = doc.page_count
    print("Number of pages: " + str(page_count))

    for pageno in range(page_count):

        il = doc.get_page_images(pageno) # get all images on page
        if len(il) > 1:
            return "More than one image per page"
        for img in il:
            image = recoverpix(doc, img)
            imgdata = image["image"]
            imgfile = os.path.join(imagedir, fpref + "%s.%s" % (pageno + 1, image["ext"]))
            fout = open(imgfile, "wb")
            fout.write(imgdata)
            fout.close()

    return "Pages extracted successfully"