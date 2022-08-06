import spacy
from spacy.util import minibatch, compounding
import random
from pathlib import Path

nlp = spacy.load("en_core_web_sm") 

ner=nlp.get_pipe('ner')

LABEL1 = "VASEREF"
LABEL2 = "HEIGHT"
LABEL3 = "COLLECTION"
LABEL4 = "PLATE"
LABEL5 = "PUBLICATION"
LABEL6 = "DESCRIPTION"
LABEL7 = "DIAMETER"
CUSTOM_LABELS = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}

TRAIN_DATA =[ ("191 Madrid 11456 (L. 442). Ht. 22", {"entities": [(0, 3, "VASEREF"),(27,33, "HEIGHT"),(4,25,"COLLECTION")]}),
              ("192 Paestum 31998, from C. Spina (1963), T. 4. Ht. 23", {"entities": [(0, 3, "VASEREF"),(47,53, "HEIGHT"),(4,39,"COLLECTION")]}),
              ("195 Paestum, from C. Spina-Gaudo (1979), T. 73. Ht. 22-5.", {"entities": [(0, 3, "VASEREF"),(48,56, "HEIGHT"),(4,39,"COLLECTION")]}),
              ("151 Paestum 21265, from C. Andriuolo (1969), T. 18. Ht. 22-5.", {"entities": [(0, 3, "VASEREF"),(52,60, "HEIGHT"),(4,43,"COLLECTION")]}),
              ("Below the handles: female heads.", {"entities": []}),
              ("*189 Once N e w York Market, Sotheby Parke Bernet, Sale Cat. 16 M a y 1980, no. 187 (ill.). Ht 22.8", {"entities": [(1, 4, "VASEREF"),(91,100, "HEIGHT"),(5,90,"COLLECTION")]}),
              ("194 Paestum, from C. Spina-Gaudo (1979), T. 70. Ht. 22.", {"entities": [(0,3, "VASEREF"),(48,54, "HEIGHT"),(4,39,"COLLECTION")]}),
              ("Paestum 6115, from C. Andriuolo-Laghetto (1955),", {"entities": []}),
              ("142 B.M. F 525. Ht. 24-5", {"entities": [(0, 3, "VASEREF"),(20,25, "HEIGHT"),(4,14,"COLLECTION")]}),
              ("144 Wurzburg 812. Ht. 18-2.", {"entities": [(0, 3, "VASEREF"),(18,26, "HEIGHT"),(4,16,"COLLECTION")]}),
              ("145 Paestum 1743, from the area of the Porta Aurea (1932). Ht. 18.", {"entities": [(0, 3, "VASEREF"),(59,65, "HEIGHT"),(3,57,"COLLECTION")]}),
              ("*148 Paestum 6107, from C. Andriuolo-Laghetto (1955), T. 64. Ht. 24.", {"entities": [(0, 3, "VASEREF"),(61,67, "HEIGHT"),(5,52,"COLLECTION")]}),
              ("149 Paestum 1742, from the area of the Porta Aurea (1932). Ht. 20-5.", {"entities": [(0, 3, "VASEREF"),(59,67, "HEIGHT"),(4,57,"COLLECTION")]}),
              ("150 B.M. F 531, from Nola. Ht. 22-4.", {"entities": [(0, 3, "VASEREF"),(27,35, "HEIGHT")]}),
              ("152 Paestum 21267, from the same tomb. Ht. 21.", {"entities": [(0, 3, "VASEREF"),(39,45, "HEIGHT"),(4,37,"COLLECTION")]}),
              ("""689 Paestum 20137, from Agropoli, T. 13. Ht. 24. Standing woman with  skewer of fruit  in r. hand and cista and fillet in 1. (White on black stripe).
""",{"entities":[(0,3,"VASEREF"),(4,32,"COLLECTION"),(41,47,"HEIGHT"),(49,149,"DESCRIPTION"),]}),
("""690 Dunedin E 23.8. Ht. 17.PPSupp, no. 280.
""",{"entities":[(0,3,"VASEREF"),(4,18,"COLLECTION"),(20,26,"HEIGHT"),(27,42,"PUBLICATION"),]}),
("""691 Paestum 21582, from C. Andriuolo (1969), T. 56. Ht. 17-5. In very bad condition. Woman seated to 1., with  skewer of fruit .
""",{"entities":[(0,3,"VASEREF"),(4,43,"COLLECTION"),(52,60,"HEIGHT"),(62,128,"DESCRIPTION"),]}),
("""694 Paestum 6013, from C. Andriuolo-Laghetto (1955), T. 22. Ht. 21. PAdd, no. A 100.
""",{"entities":[(0,3,"VASEREF"),(4,51,"COLLECTION"),(60,66,"HEIGHT"),(68,83,"PUBLICATION"),]}),
("""695 Paestum 4990, from C. Gaudo (1957), T. 14. Ht. 22. PAdd, no. A 101.
""",{"entities":[(0,3,"VASEREF"),(4,38,"COLLECTION"),(47,53,"HEIGHT"),(55,70,"PUBLICATION"),]}),
("""696 Paestum 32038, from C. Spina (1963), T. 8. Ht. 24. In bad condition. Seated half-draped woman to r., stele to 1.
""",{"entities":[(0,3,"VASEREF"),(4,39,"COLLECTION"),(47,53,"HEIGHT"),(55,116,"DESCRIPTION"),]}),
("""697 Paestum 32062, from C. Linora (1964), T. 13. Ht. 16-5. Surface in bad condition. Seated half-draped woman with cista and tambourine, stele to 1. Moving towards the style of the Painter of Naples 1778; cf. also with no. 613.
""",{"entities":[(0,3,"VASEREF"),(4,40,"COLLECTION"),(49,57,"HEIGHT"),(59,227,"DESCRIPTION"),]}),
("""*992 Madrid 11391 (L. 492). Ht. 16. PLATE 156a PP, no. 353; PPSupp, no. 472 (where associated with Painter of Naples 2585). (a) Seated draped woman with phiale and wreath, [b) seated half-draped woman with
""",{"entities":[(1,4,"VASEREF"),(5,26,"COLLECTION"),(28,34,"HEIGHT"),(47,122,"PUBLICATION"),(36,46,"PLATE"),(124,205,"DESCRIPTION"),]}),
("""*993 Paestum 5052, from C. Arcioni (1953), T. 5. Ht. 11-6, diam. 10-4. PLATE 156c PAdd, no. A 61 (where placed in the Asteas Group). (a) Seated half-draped woman with phiale and mirror, [b) female head to 1.
""",{"entities":[(1,4,"VASEREF"),(5,41,"COLLECTION"),(49,57,"HEIGHT"),(59,69,"DIAMETER"),(82,131,"PUBLICATION"),(71,81,"PLATE"),(133,207,"DESCRIPTION"),]}),
("""*995 Paestum 5401, from C. Andriuolo (1954), T. 1. Ht. 26. PLATE 156/ PAdd, no. A 290 (where associated with the Painter of Naples 2585). Draped woman with phiale, running to r., followed by nude youth with phiale. A large part of the vase between the two figures is missing.
""",{"entities":[(1,4,"VASEREF"),(5,43,"COLLECTION"),(51,57,"HEIGHT"),(70,136,"PUBLICATION"),(59,68,"PLATE"),(137,275,"DESCRIPTION"),]}),
("""*150 Paestum 20161, from Agropoli (Muoio, C. Vecchia, 1967). Ht. 24-5, diam. 34/25. PLATE 64 b
""",{"entities":[(1,4,"VASEREF"),(5,59,"COLLECTION"),(61,69,"HEIGHT"),(71,82,"DIAMETER"),(84,94,"PLATE"),]}),
("""*151 Paestum 26631, from C. Gaudo (1972), T. 2. Ht. 38-5. PLATE65
""",{"entities":[(1,4,"VASEREF"),(5,40,"COLLECTION"),(48,56,"HEIGHT"),(58,65,"PLATE"),]}),
("""*140 Louvre K 570. Ht. 20, diam. 40-5/30. PLATE 60
""",{"entities":[(1,4,"VASEREF"),(5,17,"COLLECTION"),(19,25,"HEIGHT"),(27,40,"DIAMETER"),(42,50,"PLATE"),]}),
("""*138 Kassel T 821, ex Basel and London Markets. Ht. 32-5, diam. 48-2/34 PLATE 59 c
""",{"entities":[(1,4,"VASEREF"),(5,46,"COLLECTION"),(48,56,"HEIGHT"),(58,71,"DIAMETER"),(72,82,"PLATE"),]}),
("""*136 Sydney 4901. Ht. 51, diam. 49. PLATE58
""",{"entities":[(1,4,"VASEREF"),(5,16,"COLLECTION"),(18,24,"HEIGHT"),(26,34,"DIAMETER"),(36,43,"PLATE"),]}),
("""*129A Once Market. Ht. 22-3, diam. of base 31-8. PLATE 51 b""",{"entities":[(1,5,"VASEREF"),(6,17,"COLLECTION"),(19,27,"HEIGHT"),(29,47,"DIAMETER"),(49,59,"PLATE"),]}),("""131 Salerno, from Buccino, T. 104. Diam. c. 30. Very fragmentary
""",{"entities":[(0,3,"VASEREF"),(4,33,"COLLECTION"),(35,46,"DIAMETER"),(48,64,"DESCRIPTION"),]}),
("""131 Salerno, from Buccino, T. 104. Diam. c. 30. Very fragmentary
""",{"entities":[(0,3,"VASEREF"),(4,33,"COLLECTION"),(44,46,"DIAMETER"),(48,64,"DESCRIPTION"),]}),
("""* 130 Rome, Villa Giulia 50279, from Buccino. Ht. (as preserved) 16-4; original diam. c. 34.
""",{"entities":[(0,5,"VASEREF"),(6,44,"COLLECTION"),(65,69,"HEIGHT"),(89,92,"DIAMETER"),]}),
("""*129 Malibu 81 A E 78. Ht. 71-4, diam. 60. PLATES 49-51 a
""",{"entities":[(0,4,"VASEREF"),(5,21,"COLLECTION"),(27,31,"HEIGHT"),(39,41,"DIAMETER"),(43,57,"PLATE"),]}),
("""*98 Paestum 21514, from c. Andriuolo (1969), T. 47. Ht. 16, diam. 25-5/16-5 PLATE40a'
""",{"entities":[(0,3,"VASEREF"),(4,50,"COLLECTION"),(56,58,"HEIGHT"),(66,75,"DIAMETER"),(76,84,"PLATE"),]}),
("""*52 Pontecagnano 36525, from T. 1255, Ht. 35-5, diam. 33. PLATE 29 c, d""",{"entities":[(0,3,"VASEREF"),(4,36,"COLLECTION"),(43,46,"HEIGHT"),(54,56,"DIAMETER"),(58,71,"PLATE"),]}),
("""*150 Paestum 20161, from Agropoli (Muoio, C. Vecchia, 1967). Ht. 24-5, diam. 34/25. PLATE 64 b
""",{"entities":[(1,4,"VASEREF"),(5,59,"COLLECTION"),(65,69,"HEIGHT"),(77,82,"DIAMETER"),(84,94,"PLATE"),]}),
("""*151 Paestum 26631, from C. Gaudo (1972), T. 2. Ht. 38-5. PLATE65
""",{"entities":[(1,4,"VASEREF"),(5,40,"COLLECTION"),(52,56,"HEIGHT"),(58,65,"PLATE"),]}),
("""*140 Louvre K 570. Ht. 20, diam. 40-5/30. PLATE 60
""",{"entities":[(1,4,"VASEREF"),(5,17,"COLLECTION"),(23,25,"HEIGHT"),(33,40,"DIAMETER"),(42,50,"PLATE"),]}),
("""*138 Kassel T 821, ex Basel and London Markets. Ht. 32-5, diam. 48-2/34 PLATE 59 c
""",{"entities":[(1,4,"VASEREF"),(5,46,"COLLECTION"),(52,56,"HEIGHT"),(64,71,"DIAMETER"),(72,82,"PLATE"),]}),
("""*129A Once Market. Ht. 22-3, diam. of base 31-8. PLATE 51 b
""",{"entities":[(1,5,"VASEREF"),(6,17,"COLLECTION"),(23,27,"HEIGHT"),(43,47,"DIAMETER"),(49,59,"PLATE"),]}),("""123 Ht. 13, diam. 22
""",{"entities":[(0,3,"VASEREF"),(4,10,"HEIGHT"),(12,20,"DIAMETER"),]}),
("""55 Ht. 111, diam. 66/2
""",{"entities":[(0,2,"VASEREF"),(3,10,"HEIGHT"),(12,22,"DIAMETER"),]}),
("""16 Ht. 123, diam. 999-12
""",{"entities":[(0,2,"VASEREF"),(3,10,"HEIGHT"),(12,24,"DIAMETER"),]}),
("""677 Ht. 1109, diam. 12
""",{"entities":[(0,3,"VASEREF"),(4,12,"HEIGHT"),(14,22,"DIAMETER"),]}),
("""77 Ht. 12, diam. 1112""",{"entities":[(0,2,"VASEREF"),(3,9,"HEIGHT"),(11,21,"DIAMETER"),]}),
]




dataIn = open('trainData.txt','r')
lines = dataIn.readlines()
# words = {"","","","","","",""}

labels = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}

def spaceFinder(id, VASEREF=None,COLLECTION=None,HEIGHT=None,DIAMETER=None,PUBLICATION=None,PLATE=None,DESCRIPTION=None):
  labels = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}
  words = {"VASEREF":VASEREF,"COLLECTION":COLLECTION,"HEIGHT":HEIGHT,"DIAMETER":DIAMETER,"PUBLICATION":PUBLICATION,"PLATE":PLATE,"DESCRIPTION":DESCRIPTION}
  output = "(\"\"\"{}\"\"\",{{\"entities\":[".format(lines[id])
  for key, value in words.items():   
    if value is not None:
      start = lines[id].find(str(value))
      end = start + len((str(value)))
      output = output +"({},{},\"{}\"),".format(start, end, key)
  output += "]}),"
  print(output)

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
    # Training for 50 iterations     
    for itn in range(50):
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
        # print("Losses", losses)

  output_dir = Path('./trainedModels/amapNER')
  nlp.to_disk(output_dir)
  print("Saved model to", output_dir)


trainAndRun()