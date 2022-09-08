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

input = """
*707 Paestum 5657, from C. Andriuolo (1955), T. 18. Ht. 6-5, diam. 27-5 PLATE 236a
GRFP, IIID/77, pi. 41 d.
Bass, perch, bream and torpedo, with a smaller fish, two prawns and a mussel.
Rim: wave.
"""
space_finder(input,
VASEREF="*707",
COLLECTION="Paestum 5657, from C. Andriuolo (1955), T. 18",
HEIGHT="6-5",
DIAMETER="27-5",
PUBLICATION="GRFP, IIID/77, pi. 41 d.",
PLATE="236a",
DESCRIPTION="""Bass, perch, bream and torpedo, with a smaller fish, two prawns and a mussel.
Rim: wave.""")

# space_finder(input, VASEREF="",
# COLLECTION="",
# HEIGHT="",
# DIAMETER=None,
# PUBLICATION=None,
# PLATE=None,
# DESCRIPTION="""""")