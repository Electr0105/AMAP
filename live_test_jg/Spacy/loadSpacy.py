import spacy

def spacy_run(value):
	"""Basic run function for spacy, load the saved model and predict"""
	output_dir = "Spacy/amapNER"
	nlp_load = spacy.load(output_dir)
	doc = nlp_load(value)
	store = []
	for ent in doc.ents:
		store.append(str(ent.label_) + ": " + str(ent))
	return store