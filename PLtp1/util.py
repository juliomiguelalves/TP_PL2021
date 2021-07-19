import re


def acentos(matchobj):
    res = ''
    char = matchobj.group(1)
    if char == 'a':
        res = "á"
    elif char == 'A':
        res = "Á"
    elif char == 'e':
        res = "é"
    elif char == 'E':
        res = "É"
    elif char == 'i':
        res = "í"
    elif char == 'I':
        res = "Í"
    elif char == 'o':
        res = "ó"
    elif char == 'O':
        res = "Ó"
    elif char == 'u':
        res = "ú"
    elif char == 'U':
        res = "Ú"
    return res


def tils(matchobj):
    res = ''
    char = matchobj.group(1)
    if char == 'a':
        res = "ã"
    elif char == 'A':
        res = "Ã"
    elif char == 'o':
        res = "õ"
    elif char == 'O':
        res = "Õ"
    elif char == 'n':
        res = "ñ"
    elif char == 'N':
        res = "Ñ"
    return res


def normalize_alphas(target):
    target = re.sub(r'\\T', 'T', target)
    target = re.sub(r'\\\'([AaEeIiOoUu])', acentos, target)
    target = re.sub(r'\\~([AaOoNn])', tils, target)
    return target


def normalize_symbols(text):
    return re.sub(r'\\([$#&])', r'\1', text)


def stripSpaces(text):
    text = re.sub(r'^ +', r'', text)
    text = re.sub(r' +$', r'', text)
    return text


def write_dict_to_html(list_, file):
    file.write("<!DOCTYPE html>\n<html>\n\t<body>\n\t\t<ol>\n")
    for key in sorted(list_):
        file.write("\t\t\t<li>" + key + " : " + str(list_[key]) + "</li>\n")
    file.write('\t\t</ol>\n\t</body>\n</html>\n')


def write_dictlist_to_html(matrix, file):
    file.write("<!DOCTYPE html>\n<html>\n\t<body>\n\t\t<ol>\n")
    for key in sorted(matrix):
        file.write("\t\t\t<li>" + key + "</li>\n\t\t\t<ul>\n")
        for value in sorted(matrix[key]):
            file.write("\t\t\t\t<li>" + value + "</li>\n")
        file.write('\t\t\t</ul>\n')
    file.write('\t\t</ol>\n\t</body>\n</html>\n')


def add_padding(string, padding):
    return re.sub(r'\n', rf'\n{padding}', string)


def write_dictlist_to_json(matrix, file):
    file.write("{\n")
    donit = True
    for entry in matrix:
        if donit:
            donit = False
        else:
            file.write(',\n')
        donit2 = True
        file.write('\t"' + entry + "\" : [\n\t\t")
        for node in matrix[entry]:
            if donit2:
                donit2 = False
            else:
                file.write(',')
            file.write('' + add_padding(node, '\t\t'))
        file.write('\n\t]')
    file.write("\n}")
