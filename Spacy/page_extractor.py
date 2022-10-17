import pdfplumber

write_file = open('write_RVP.py','a')
page_values = open('page_extraction.txt','w')
pdf = pdfplumber.open("RVPfixed.pdf")
page_text = pdf.pages[230].extract_text()

# Part 1
page_values.write(page_text)
# Part 2
vases = [
"""""",
]


shapes = []

def writer():
    entities = ""
    counter = 1
    for vase in vases:
        try:
            start = page_text.index(vase)
            print(start)
            end = len(vase) + start
            counter += 1
            entities += f"({start}, {end}, \"VASE\"),"
        except:
            print("VASE number " + str(counter) + " Failed :)")

    counter = 1
    for shape in shapes:
        try:
            start = page_text.index(shape)
            print(start)
            end = len(shape) + start
            counter += 1
            entities += f"({start}, {end}, \"SHAPE\"),"
        except:
            print("SHAPE number " + str(counter) + " Failed :)")

    write_output = "(\"\"\"" + page_text + "\"\"\"," + "{\"entities\": [" + entities + "]}),"
    write_file.write(write_output)

# writer()
