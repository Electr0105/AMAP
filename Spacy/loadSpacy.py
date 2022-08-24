import spacy

def spacy_run(value):
	"""Basic run function for spacy, load the saved model and predict"""
	output_dir = "Spacy/TrainedModels/model_50k"
	nlp_load = spacy.load(output_dir)
	doc = nlp_load(value)
	store = {}
	for ent in doc.ents:
		label = str(ent.label_)
		value = str(ent)
		# "{}: {}".format(str(ent.label_), str(ent))
		store.update({label:value})
	return store

def filler(filled_dict):
    test = {"VASEREF":"","COLLECTION":"","HEIGHT":"","DIAMETER":"","PLATE":"","DESCRIPTION":"","PUBLICATION":"","SHAPE":""}
    update = {"VASEREF":"","COLLECTION":"","HEIGHT":"","DIAMETER":"","PLATE":"","DESCRIPTION":"","PUBLICATION":"","SHAPE":""}
    for key in test:
        if key in filled_dict:
            update.update([(key,filled_dict[key])])
    return update