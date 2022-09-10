import random
from pathlib import Path
from spacy.util import minibatch, compounding
import spacy

train_file = open('train_data.txt','r', encoding="utf-8")

for x in train_file.readlines():
    print(x)