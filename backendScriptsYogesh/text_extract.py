from PyPDF2 import PdfFileReader
from pathlib import Path

#Create pdf file reader object """
pdf = PdfFileReader('RVPfixed.pdf')

#TWO 2 TO EXTRACT
#Step 1: Grab the page(s)
page1_object = pdf.getPage(0)
print(page1_object)

#Step 2: extract
page1_text = page1_object.extractText()
print(page1_text)

#Combine text save as txt
with Path('RVPfixed.txt').open(mode='w') as output_file:
    text = ''
    for page in pdf.pages:
        text+=page.extractText()
    output_file.write(text)

