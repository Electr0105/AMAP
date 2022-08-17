import csv
import spacy
import difflib

class bcolors:
    """Collection for printing colours"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

open_file = open("test_values.csv",'r',encoding='utf-8')
csv_file = list(csv.reader(open_file))
csv_file_headers = csv_file[0]
csv_file.remove(['Input', 'VASEREF', 'COLLECTION', 'HEIGHT', 'DIAMETER',
                    'PLATE', 'DESCRIPTION', 'PUBLICATION'])

OUTPUT_DIR = "TrainedModels/small_test_10k"
NLP_LOAD = spacy.load(OUTPUT_DIR)

collection = []
for value in csv_file:
    doc = NLP_LOAD(value[0])
    label_and_value = []
    for ent in doc.ents:
        label_and_value.append(f"{ent.label_}: {ent} ")
    collection.append(label_and_value)

def tester_function(doc_element):
    FULL_TOTAL = 0
    FULL_PASSED = 0
    for line in range(0, len(collection)):
        RUN_TOTAL = len(collection[line])
        FULL_TOTAL += RUN_TOTAL
        RUN_PASSED = 0
        collection_two = []
        for header_element, line_element  in zip(csv_file_headers, csv_file[line]):
            collection_two.append(f"{header_element}: {line_element}")

        for line1, line2 in zip(collection[line], collection_two[1:]):
            print(bcolors.OKCYAN)
            print("Expected: " + str(line2))
            print("Recieved: " + str(line1))
            if line1.strip() == line2.strip():
                print(bcolors.OKGREEN + "PASSED")
                RUN_PASSED += 1
            else:
                print(bcolors.FAIL + '\n'.join(difflib.ndiff([line1], [line2])))
                print(bcolors.OKCYAN)
        print("***************")
        print("Pass Rate: " + "{:.2f}".format(RUN_PASSED/RUN_TOTAL*100) + "%")
        print(f"{RUN_PASSED} out of {RUN_TOTAL}")
        FULL_PASSED += RUN_PASSED
    print("***************")
    print("***************")
    print(f"Ran {len(collection)} tests")
    print("Total Pass Rate: " + "{:.2f}".format(FULL_PASSED/FULL_TOTAL*100) + "%")
    print(f"{FULL_PASSED} out of {FULL_TOTAL}")

tester_function('Line')
