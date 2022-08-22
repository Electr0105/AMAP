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