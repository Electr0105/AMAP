import random
from pathlib import Path
from spacy.util import minibatch, compounding
import spacy
from train_data import TRAIN_DATA_02
from datetime import datetime
nlp = spacy.load("en_core_web_sm")
TRAIN_DATA = TRAIN_DATA_02
ner=nlp.get_pipe('ner')


time_now = datetime.now()

LABEL1 = "VASEREF"
LABEL2 = "HEIGHT"
LABEL3 = "COLLECTION"
LABEL4 = "PLATE"
LABEL5 = "PUBLICATION"
LABEL6 = "DESCRIPTION"
LABEL7 = "DIAMETER"
CUSTOM_LABELS = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}

# dataIn = open('trainData.txt','r')
# lines = dataIn.readlines()
# # words = {"","","","","","",""}

# labels = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}

# def spaceFinder(id, VASEREF=None,COLLECTION=None,HEIGHT=None,DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION=None):
#   labels = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}
#   words = {"VASEREF":VASEREF,"COLLECTION":COLLECTION,"HEIGHT":HEIGHT,"DIAMETER":DIAMETER,"PUBLICATION":PUBLICATION,"PLATE":PLATE,"DESCRIPTION":DESCRIPTION}
#   output = "(\"\"\"{}\"\"\",{{\"entities\":[".format(lines[id])
#   for key, value in words.items():   
#     if value is not None:
#       start = lines[id].find(str(value))
#       end = start + len((str(value)))
#       output = output +"({},{},\"{}\"),".format(start, end, key)
#   output += "]}),"
#   print(output)

# spaceFinder(id, VASEREF=None,COLLECTION=None,HEIGHT=None,DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION=None)

# spaceFinder(0, VASEREF="689",COLLECTION="Paestum 20137, from Agropoli",HEIGHT="Ht. 24",DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION="Standing woman with  skewer of fruit  in r. hand and cista and fillet in 1. (White on black stripe).")
# spaceFinder(1, VASEREF="690",COLLECTION="Dunedin E 23.8",HEIGHT="Ht. 17",DIAMETER=None,PUBLICATION="PPSupp, no. 280",PLATE=None,DESCRIPTION=None)
# spaceFinder(2, VASEREF="691",COLLECTION="Paestum 21582, from C. Andriuolo (1969)",HEIGHT="Ht. 17-5",DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION="In very bad condition. Woman seated to 1., with  skewer of fruit .")
# spaceFinder(3, VASEREF="694",COLLECTION="Paestum 6013, from C. Andriuolo-Laghetto (1955)",HEIGHT="Ht. 21",DIAMETER=None,PUBLICATION="PAdd, no. A 100",PLATE=None,DESCRIPTION=None)
# spaceFinder(4, VASEREF="695",COLLECTION="Paestum 4990, from C. Gaudo (1957)",HEIGHT="Ht. 22",DIAMETER=None,PUBLICATION="PAdd, no. A 101",PLATE=None,DESCRIPTION=None)
# spaceFinder(5, VASEREF="696",COLLECTION="Paestum 32038, from C. Spina (1963)",HEIGHT="Ht. 24",DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION="In bad condition. Seated half-draped woman to r., stele to 1.")
# spaceFinder(6, VASEREF="697",COLLECTION="Paestum 32062, from C. Linora (1964)",HEIGHT="Ht. 16-5",DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION="Surface in bad condition. Seated half-draped woman with cista and tambourine, stele to 1. Moving towards the style of the Painter of Naples 1778; cf. also with no. 613.")
# spaceFinder(7, VASEREF="992",COLLECTION="Madrid 11391 (L. 492)",HEIGHT="Ht. 16",DIAMETER=None,PUBLICATION="PP, no. 353; PPSupp, no. 472 (where associated with Painter of Naples 2585)",PLATE="PLATE 156a",DESCRIPTION="(a) Seated draped woman with phiale and wreath, [b) seated half-draped woman with")
# spaceFinder(8, VASEREF="993",COLLECTION="Paestum 5052, from C. Arcioni (1953)",HEIGHT="Ht. 11-6",DIAMETER="diam. 10-4",PUBLICATION="PAdd, no. A 61 (where placed in the Asteas Group)",PLATE="PLATE 156c",DESCRIPTION="(a) Seated half-draped woman with phiale and mirror, [b) female head to 1.")
# spaceFinder(9, VASEREF="995",COLLECTION="Paestum 5401, from C. Andriuolo (1954)",HEIGHT="Ht. 26",DIAMETER=None,PUBLICATION="PAdd, no. A 290 (where associated with the Painter of Naples 2585)",PLATE="PLATE 156",DESCRIPTION=" Draped woman with phiale, running to r., followed by nude youth with phiale. A large part of the vase between the two figures is missing.")

# spaceFinder(17, VASEREF="150",COLLECTION="Paestum 20161, from Agropoli (Muoio, C. Vecchia, 1967)",HEIGHT="24-5",DIAMETER="34/25",PUBLICATION=None,PLATE="PLATE 64 b",DESCRIPTION=None)
# spaceFinder(18, VASEREF="151",COLLECTION="Paestum 26631, from C. Gaudo (1972)",HEIGHT="38-5",DIAMETER=None,PUBLICATION=None,PLATE="PLATE65",DESCRIPTION=None)
# spaceFinder(19, VASEREF="140",COLLECTION="Louvre K 570",HEIGHT="20",DIAMETER="40-5/30",PUBLICATION=None,PLATE="PLATE 60",DESCRIPTION=None)
# spaceFinder(20, VASEREF="138",COLLECTION="Kassel T 821, ex Basel and London Markets",HEIGHT="32-5",DIAMETER="48-2/34",PUBLICATION=None,PLATE="PLATE 59 c",DESCRIPTION=None)
# spaceFinder(21, VASEREF="136",COLLECTION="Sydney 4901",HEIGHT="51",DIAMETER="49",PUBLICATION=None,PLATE="PLATE58",DESCRIPTION=None)
# spaceFinder(22, VASEREF="129A",COLLECTION="Once Market",HEIGHT="22-3",DIAMETER="31-8",PUBLICATION=None,PLATE="PLATE 51 b",DESCRIPTION=None)

# spaceFinder(24, VASEREF="131",COLLECTION="Salerno, from Buccino, T. 104",HEIGHT=None,DIAMETER="30",PUBLICATION=None,PLATE=None,DESCRIPTION="Very fragmentary")
# spaceFinder(25, VASEREF="* 130",COLLECTION="Rome, Villa Giulia 50279, from Buccino",HEIGHT="16-4",DIAMETER="34",PUBLICATION=None,PLATE=None,DESCRIPTION=None)
# spaceFinder(26, VASEREF="*129",COLLECTION="Malibu 81 A E 78",HEIGHT="71-4",DIAMETER="60",PUBLICATION=None,PLATE="PLATES 49-51 a",DESCRIPTION=None)
# spaceFinder(27, VASEREF="*98",COLLECTION="Paestum 21514, from c. Andriuolo (1969), T. 47",HEIGHT="16",DIAMETER="25-5/16-5",PUBLICATION=None,PLATE="PLATE40a",DESCRIPTION=None)
# spaceFinder(28, VASEREF="*52",COLLECTION="Pontecagnano 36525, from T. 1255",HEIGHT="35-5",DIAMETER="33",PUBLICATION=None,PLATE="PLATE 29 c, d",DESCRIPTION=None)

# spaceFinder(30, VASEREF="123",COLLECTION=None,HEIGHT="Ht. 13",DIAMETER="diam. 22",PUBLICATION=None,PLATE=None,DESCRIPTION=None)
# spaceFinder(31, VASEREF="55",COLLECTION=None,HEIGHT="Ht. 111",DIAMETER="diam. 66/2",PUBLICATION=None,PLATE=None,DESCRIPTION=None)
# spaceFinder(32, VASEREF="16",COLLECTION=None,HEIGHT="Ht. 123",DIAMETER="diam. 999-12",PUBLICATION=None,PLATE=None,DESCRIPTION=None)
# spaceFinder(33, VASEREF="677",COLLECTION=None,HEIGHT="Ht. 1109",DIAMETER="diam. 12",PUBLICATION=None,PLATE=None,DESCRIPTION=None)
# spaceFinder(34, VASEREF="77",COLLECTION=None,HEIGHT='Ht. 12',DIAMETER="diam. 1112",PUBLICATION=None,PLATE=None,DESCRIPTION=None)

# spaceFinder()



# print(TRAIN_DATA[1][0][22:26])
# label = "COLLECTION"
# word = {"570"}
# for i in range(0, len(TRAIN_DATA)):
#   for x in word:
#     start = TRAIN_DATA[i][0].find(x)
#     last = start + len(x)
#     if(start != -1):
#       print("ID: {}     ,({},{},\"{}\")".format(i, str(start),str(last),label))
def trainAndRun():
  for x in CUSTOM_LABELS:
    ner.add_label(x)
  # ner.add_label(LABEL1)
  # ner.add_label(LABEL2)
  # ner.add_label(LABEL3)
  optimizer = nlp.resume_training()
  move_names = list(ner.move_names)

  # List of pipes you want to train
  pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

  # List of pipes which should remain unaffected in training
  other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

  with nlp.disable_pipes(*other_pipes) :

    sizes = compounding(1.0, 4.0, 1.001)
    # Training for 50000 iterations     
    for itn in range(50000):
      # shuffle examples before training
      random.shuffle(TRAIN_DATA)
      # batch up the examples using spaCy's minibatch
      batches = minibatch(TRAIN_DATA, size=sizes)
      # ictionary to store losses
      losses = {}
      for batch in batches:
        texts, annotations = zip(*batch)
        # Calling update() over the iteration
        nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)

  output_dir = Path('./TrainedModels/model_50k')
  nlp.to_disk(output_dir)
  print("Saved model to", output_dir)


trainAndRun()

time_after = datetime.now()
print("Time 1: " + str(time_now))
print("Time 2: " + str(time_after))
print("Time 3: " + str(time_after - time_now))
