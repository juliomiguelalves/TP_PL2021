import re
import util
from graphviz import Digraph


def read_all_entries(text):
    # Normalizations
    text = re.sub(r'^%.*$', r'', text)  # Remove comments
    text = util.normalize_alphas(text)  # Process \' and \~ into actual chars
    text = util.normalize_symbols(text)
    text = re.sub(r'[ \t]+', r' ', text)  # No redundant spaces

    result = []
    for (gp, _) in re.findall(r'(@(\\@|[^@])+})', text):  # It's not 100% correct
        result.append(gp)
    return result


# Calcular o número de entradas por categoria
# apresente a listagem em formato HTML por ordem alfabética
def funcionalidade_a(entrylist):
    res = dict()
    for entry in entrylist:
        y = re.match(r'@(\w+)', entry)
        if y:
            # the capitalize method desensitizes (upper/lower)cases
            entryclass = y.group(1).capitalize()
            if entryclass in res:
                res[entryclass] = res[entryclass] + 1
            else:
                res[entryclass] = 1
    return res


# Criar um índice de autores, que mapeie cada autor nos respectivos
# registos identificados pela respectiva chave de citação
def funcionalidade_b(entrylist):
    res = dict()
    for entry in entrylist:
        key = re.match(r'@\w+{([^,]+)', entry).group(1)
        authors = re.search(r'author[ \t]*=[ \t]*({+ *((\\}|[^}])*)}+|\" *((\\\"|[^"])*)\")', entry)
        if key and authors:
            if authors.group(2):
                authors = authors.group(2)
            else:
                authors = authors.group(4)
            authors = re.sub(r'[\n\r\t ]+', r' ', authors)
            for author in re.split(r' +and +', authors):
                author = util.stripSpaces(author)
                author = re.match(r'((.|\n)*) ?$', author).group(1)
                if author not in res:
                    res[author] = [key]
                else:
                    res[author].append(key)
    return res


# Transforme cada registo num documento JSON válido;
# a BD original deve ser então um documento JSON válido formado por uma lista de registos.
def funcionalidade_c(entrylist):
    output = dict()

    for entry in entrylist:
        entry = re.sub(r'\\\w+{([^}]+?)}', r'\1', entry)

        obj = re.match(r'@(\w+)', entry)
        if obj:
            category = obj.group(1).lower()

            obj = re.search(r'\{(\w+),', entry)
            if obj:
                json_entry = '{\n\t"label" : "' + obj.group(1) + '",\n'

                for (tag, _, brackets, weird_brackets, _, marks, num) in re.findall(
                        r'(\w+)[ \n\t]*=[ \n\t]*({((.|\n)*?)},|{([^}]*)}|\"([^"]*)\"|([0-9]*)),?', entry):
                    if obj:
                        if brackets:
                            target = brackets
                        elif weird_brackets:
                            target = weird_brackets
                        elif marks:
                            target = marks
                        elif num:
                            target = num
                        else:
                            target = ''
                        if target.isnumeric():
                            json_entry += '\t"' + tag + '" : ' + target + ',\n'
                        else:
                            target = re.sub(r'\\?\"', '\\"', target)
                            target = re.sub(r'\n', r'\\n', target)
                            json_entry += '\t"' + tag + '" : "' + target + '",\n'
                json_entry = json_entry[:-2] + '\n}'

                if category not in output:
                    output[category] = [json_entry]
                else:
                    output[category].append(json_entry)
    return output


# Construa um Grafo que mostre, para um dado autor todos os autores que publicam
# normalmente com o autor em causa.
def funcionalidade_d(nome_autor, entrylist):
    dot = Digraph(name=nome_autor, strict=True)
    for entry in entrylist:
        author = re.search(r'author[ \t]*=[ \t]*({+ *((\\}|[^}])*)}+|\" *((\\\"|[^"])*)\")', entry)
        if author:
            if author.group(2):
                authors = author.group(2)
            else:
                authors = author.group(3)
            if authors:
                authors = re.sub(r'[\n\r\t ]+', r' ', authors)
                authors = re.split(r' +and +', authors)
                if nome_autor in authors:
                    for name in authors:
                        name = util.stripSpaces(name)
                        if (not (name == " ")) and (not (name.__str__ is None)) and not (name == nome_autor):
                            if not (name in dot.source):
                                dot.node(name.__str__())
                                dot.edge(nome_autor, name)
    return dot
