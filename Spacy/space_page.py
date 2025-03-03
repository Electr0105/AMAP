# Written by Jackson Gleeson
# For PRA/B in 2022

import spacy

def spacy_run(value):
	"""Basic run function for spacy, load the saved model and predict"""
	output_dir = "TrainedModels/page_model_3k"
	nlp_load = spacy.load(output_dir)
	doc = nlp_load(value)
	store = {}
	for ent in doc.ents:
		label = str(ent.label_)
		value = str(ent)
		# "{}: {}".format(str(ent.label_), str(ent))
		store.update({label:value})
	return store
input = """
MINOR VASES FROM THE ASTEAS-PYTHON WORKSHOP  199
546 Paestum 21973, from C. Andriuolo (1969), T. 178. Ht. 20.
Nude youth running to r., with thyrsus in r. hand, drapery over 1. arm and 'skewer of
fruit' in 1.
547  Paestum 31863, from Gromola (Strecara—1960), T. 1. Ht. 19.
Nude youth, with egg in 1. hand and cista in r., moving to 1. and looking r.
548  Vienna 932. Ht. 19.
PPSupp, no. 231.
Youth with 'skewer of fruit', and drapery over 1. arm.
549  Avignon, Musee Calvet. Ht. 17-8.
PAdd, no. A 55.
Nude youth bending forward over 1. foot raised on white tendril between two stelai;
wreath in r. hand, mirror in 1.
550  Paestum 21143, from C. Andriuolo (1969), T. 1. Ht. 18.
Seated half-draped youth, with 'skewer of fruit' and mirror.
551  Paestum 21441, from C. Andriuolo (1969), T. 38. Ht. 19-5. Surfact worn.
Half-draped youth seated on tendril, with wreath and cista.
552  Paestum, from Roccadaspide Tempalta (1984), T. 1. Ht. 20.
Seated half-draped youth to r., with cista of eggs and fillet in 1.
553  Paestum 5577, from C. Andriuolo (1954), T. 47. Ht. 19-5.
PAdd, no. A 54.
Young satyr seated on white dotted mound, 'skewer of fruit' in 1. hand, and thyrsus in r.
554  Once Basel Market, Kunsthaus zum Gellert, Sale Cat. no. 24, 26-28 Nov. 1981, no. 2282, ill.
on p. 116. Ht. 22.
Young satyr, with wreath in either hand, bending forward in front of stele.
(d) With Eros
555 Once London Market, Christie's, South Kensington, Sale Cat. 18 May 1983, no. 121, ill. on
pi. 3. Ht. 25.
Eros with phiale and wreath, bending forward over r. leg, resting on altar; duck to 1.
556  Padula, from Valle Pupina, T. 16. Ht. 21 (as restored).
ArchReps 1964, p. 38, fig. 5; Apollo III-IV, 1963^, ill. on plate facing p. 193 (showing
tomb complex).
Eros with r. foot raised.
557  Basel, Historisches Museum 1906.268. Ht. 21.
Eros bending forward to 1. over r. foot on white tendril, 'skewer of fruit' in r. hand; stele
to r.
Close to Asteas.
558  Louvre CA 2270, Ht. 21.
PP, no. 173; PPSupp, no. 221.
Eros, with dish of eggs and 'skewer of fruit', at stele.
559  Once London Market, Charles Ede Ltd. Ht. 18-4.
Cat. 74, no. 729 (ill.); Collecting Antiquities, p. 23, fig. 51.
Eros running to 1. with phiale.
560  Madrid 11146 (L. 425). Ht. 20.
PP, no. 172; PPSupp, no. 220.
Eros running to r. with wreath and phiale.
561  Paestum 32243, from Spinazzo (1973), T. 9. Ht. 21.
Eros striding to 1. with wreath.
562  Pontecagnano 26325, from T. 450.
Eros running to I. with phiale and fillet.
Below the handles: owls.
563  Naples 736 (inv. 82737). Ht. 21.
PAdd, no. A 31.
Eros, with phiale and mirror, moving to r. and looking back to 1.
The fired clay looks more Campanian, but the Eros is very Paestan.
"""
tester = spacy_run(input)
print(tester)