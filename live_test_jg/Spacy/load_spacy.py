import spacy
class load_spacey:
	def spacy_run(self, value):
		"""Basic run function for spacy, load the saved model and predict"""
		open_file = open('Spacy/spacy_output.txt','w', encoding="utf-8")
		output_dir = "Spacy/TrainedModels/small_test_10000"
		nlp_load = spacy.load(output_dir)
		doc = nlp_load(value)
		store = []
		for ent in doc.ents:
			label_and_value = "{} : {}".format(str(ent.label_), str(ent))
			store.append(label_and_value)
			open_file.write(label_and_value)
		open_file.close()
		return store