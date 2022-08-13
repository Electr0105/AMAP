open_file = open('formated_data.txt','a')

def space_finder(input=None, VASEREF=None,COLLECTION=None,HEIGHT=None,DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION=None):
    labels = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}
    words = {"VASEREF":VASEREF,"COLLECTION":COLLECTION,"HEIGHT":HEIGHT,"DIAMETER":DIAMETER,"PUBLICATION":PUBLICATION,"PLATE":PLATE,"DESCRIPTION":DESCRIPTION}
    output = "(\"\"\"{}\"\"\",{{\"entities\":[".format(input)
    for key, value in words.items():   
        if value is not None:
            start = input.find(str(value))
            end = start + len((str(value)))
            output = output +"({},{},\"{}\"),".format(start, end, key)
    output += "]}),"
    print(output)
    # open_file.write(output + "\n")

input = """*995 Paestum 5401, from C. Andriuolo (1954), T. 1. Ht. 26. PLATE 156/ PAdd, no. A 290 (where associated with the Painter of Naples 2585).
Draped woman with phiale, running to r., followed by nude youth with phiale. A large part of the vase between the two figures is missing.
"""
space_finder(input,
VASEREF="*995",
COLLECTION="Paestum 5401, from C. Andriuolo (1954), T. 1",
HEIGHT="26",
DIAMETER=None,
PUBLICATION="PAdd, no. A 290 (where associated with the Painter of Naples 2585)",
PLATE="156/",
DESCRIPTION="Draped woman with phiale, running to r., followed by nude youth with phiale. A large part of the vase between the two figures is missing.")

# space_finder(input, VASEREF="",
# COLLECTION="",
# HEIGHT="",
# DIAMETER=None,
# PUBLICATION=None,
# PLATE=None,
# DESCRIPTION="""""")