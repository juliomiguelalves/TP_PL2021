import sys
import tp1
import util

default_file = 'exemplo-utf8.bib'
input_stream = sys.stdin
is_stdout = True
output_stream = sys.stdout
entrylist = []


def inputTarget():
    global input_stream, entrylist
    # Read all file Content
    text = input_stream.read()
    entrylist = tp1.read_all_entries(text)


def menu():
    global input_stream, output_stream
    print("Escolha a funcionalidade que deseja executar:\n")
    print("a - Calcular o número de entradas por categoria")
    print("b - Criar um índice de autores")
    print("c - Transformar cada registo num documento JSON válido")
    print("d - Construir um Grafo")
    print("i - Mudar ficheiro de entrada")
    print("o - Mudar ficheiro de saída")
    print("e - Sair")
    print("\nFicheiro de entrada atual : " + input_stream.name)
    if is_stdout:
        print("O programa irá imprimir as funcionalidades na consola")
    else:
        print("Ficheiro de saída atual : " + output_stream.name)


def init_ui():
    global input_stream, default_file
    input_stream = open(default_file, "r", encoding='utf-8')


def ui():
    global input_stream, output_stream, is_stdout

    op = ' '
    while op != 'e':
        menu()
        op = input(">> ")
        if op == 'a':
            print("Funcionalidade a")
            call_A()
        elif op == 'b':
            print("Funcionalidade b")
            call_B()
        elif op == 'c':
            print("Funcionalidade c")
            call_C()
        elif op == 'd':
            print("Funcionalidade d")
            nome_autor = input("Indique o autor: ")
            call_D(nome_autor)
        elif op == 'i':
            file = input("Indique novo ficheiro de entrada: ")
            input_stream = open(file, "r", encoding='utf-8')
            inputTarget()
        elif op == 'o':
            file = input("Indique novo ficheiro de saída: ")
            if is_stdout:
                is_stdout = False
            else:
                output_stream.close()
            output_stream = open(file, "w", encoding='utf-8')
        elif op == 'e':
            pass
        else:
            print("Opção inválida!")
        input("\nClique no enter para continuar")


def call_A():
    global entrylist, output_stream
    util.write_dict_to_html(tp1.funcionalidade_a(entrylist), output_stream)
    output_stream.flush()


def call_B():
    global entrylist, output_stream
    util.write_dictlist_to_html(tp1.funcionalidade_b(entrylist), output_stream)
    output_stream.flush()


def call_C():
    global entrylist, output_stream
    util.write_dictlist_to_json(tp1.funcionalidade_c(entrylist), output_stream)
    output_stream.flush()


def call_D(nome_autor):
    global entrylist
    dot = tp1.funcionalidade_d(nome_autor, entrylist)
    dot.format = 'png'
    dot.unflatten().view()


# Main
argc = len(sys.argv)
uib = False

if argc == 1 or ('gui' in sys.argv):
    init_ui()
    uib = True

inputTarget()

if uib:
    ui()
else:
    if sys.argv[1] == 'a' or sys.argv[1] == 'A':
        call_A()
    elif sys.argv[1] == 'b' or sys.argv[1] == 'B':
        call_B()
    elif sys.argv[1] == 'c' or sys.argv[1] == 'C':
        call_C()
    elif sys.argv[1] == 'd' or sys.argv[1] == 'D':
        if argc > 2:
            call_D(sys.argv[2])
        else:
            print("Missing author")

input_stream.close()
output_stream.close()
