import random
from pathlib import Path
from spacy.util import minibatch, compounding
import spacy
from write_RVP import TRAIN_DATA_01
from datetime import datetime

nlp = spacy.load("en_core_web_sm")
TRAIN_DATA = TRAIN_DATA_01
ner=nlp.get_pipe('ner')


time_now = datetime.now()

LABEL1 = "VASEREF"
LABEL2 = "HEIGHT"
LABEL3 = "COLLECTION"
LABEL4 = "PLATE"
LABEL5 = "PUBLICATION"
LABEL6 = "DESCRIPTION"
LABEL7 = "DIAMETER"
# CUSTOM_LABELS = {"VASEREF","COLLECTION","HEIGHT","DIAMETER","PUBLICATION","PLATE","DESCRIPTION"}
CUSTOM_LABELS = {"VASE","SHAPE"}

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
    for itn in range(3000):
      # shuffle examples before training
      random.shuffle(TRAIN_DATA)
      # batch up the examples using spaCy's minibatch
      batches = minibatch(TRAIN_DATA, size=sizes)
      # ictionary to store losses
      losses = {}
      for batch in batches:
        texts, annotations = zip(*batch)
        # Calling update() over the iteration
        nlp.update(texts, annotations, sgd=optimizer, drop=0.1, losses=losses)

  output_dir = Path('./TrainedModels/page_model_3k')
  nlp.to_disk(output_dir)
  print("Saved model to", output_dir)


trainAndRun()

time_after = datetime.now()
print("Time 1: " + str(time_now))
print("Time 2: " + str(time_after))
print("Time 3: " + str(time_after - time_now))
