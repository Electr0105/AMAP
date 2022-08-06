# Load the saved model and predict
import spacy
from pathlib import Path
from spacy.language import Language

output_dir = Path('./trainedModels/amapNER')
print("Loading from", output_dir)
nlpLoad = spacy.load(output_dir)
# openFile = open('pageTrainData.txt','r')
# lines =""
# for x in openFile.readlines():
#   lines +=x
# doc = nlpLoad(lines)
# Test strings
doc = nlpLoad("""*189 Once N e w York Market, Sotheby Parke Bernet, Sale Cat. 16 M a y 1980, no. 187 (ill.). Ht.
34-5. PLATE 184 c
Body: (a) T w o nude women, 1. with phiale, r. with alabastron, at a laver, in which is a
white bird (swan ?), [b) seated woman holding cista.
Shoulder: white female heads in profile to 1. between (a) plastic heads with white flesh
and yellow hair, [b) conical knobs.
Lid—in two parts: (i) lekanis, with fan-palmettes, (ii) lebes with female head, wearing
black and white dotted sphendone.
Closely comparable to no. 188.""")

store = {}
for ent in doc.ents:
    print(str(ent.label_) + ": " + str(ent))

height = ""

for x in doc.ents:
  if x.label_ == "DIAMETER":
    height += str(x)

    