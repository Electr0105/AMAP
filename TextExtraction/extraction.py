from Spacy.loadSpacy import spacy_run, filler
from zipfile import ZipFile
from sql_scripts import insert_to_DB

def ref_extractor(input_zip):

    zip_file = ZipFile(input_zip)

    for file in zip_file.filelist:
        all_text = zip_file.read(file).decode("utf-8")
        all_lines = all_text.replace('\r','').split('\n')

        all_words = []
        for word in all_lines[1:]:
            all_words.append(word.split('\t'))

        all_refs = []
        for word in all_words[:-1]:
            if(int(word[7]) > 400 and int(word[6]) < 500) and word[11] != '' and word[11].replace("*",'').isdigit() and len(word[11]) < 4:
                all_refs.append(word)

        for ref in all_refs:
            output_string = ""
            for word in all_words[:-1]:
                if (int(word[7]) - 15) < int(ref[7]) < (int(word[7]) + 15):
                    output_string += str(word[11]) + " "
            output = spacy_run(output_string.strip())
            insert_to_DB(filler(output))