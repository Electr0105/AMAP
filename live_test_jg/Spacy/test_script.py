import csv
import spacy

open_file = open("test_values.csv",'r',encoding='utf-8')
reader = csv.reader(open_file)

OUTPUT_DIR = "amapNER"
NLP_LOAD = spacy.load(OUTPUT_DIR)

values = []

next(reader, None)

for value in reader:
    doc = NLP_LOAD(value[0])
    label_and_value = ""
    for ent in doc.ents:
        if ent is not None:
            label_and_value += "{} : {} | ".format(str(ent.label_), str(ent))
    print(label_and_value)
