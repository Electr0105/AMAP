def text_extractor(file_object):
    file = open(file_object,'r')
    lines = ""
    for x in file:
        lines.join(x)
    return lines