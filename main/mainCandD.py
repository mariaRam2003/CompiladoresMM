from regex.regex import evaluar
from Automatas.Thompson import *
from errors.Errors import *
from ShuntingYard.parse_tree_builder import *
from errors.ErrorsInFile import *
import re
from Simulator import *

tabla = {} # Tabla para guardar las declaraciones con let.
archivo = "../examples/ex3.txt"

tabla_res = {} # Tabla para guardar las palabras reservadas.

res_list = [] #Lista para guardar las palabras reservadas.

# Abriendo el archivo expresiones.yal para leer su contenido.
with open("../examples/ex3.yal", "r", encoding='utf-8') as file:
    data = file.read() # Leyendo la data del archivo.
    
    #print("Data: ", data)

    # Expresión regular para encontrar las variables que se declaran con let.
    regex_let = r"let (\w+) = (.*)"

    # Encontrando las variables que se declaran con let.
    variables = re.findall(regex_let, data)

    #print("Variables: ", variables)
    for var in variables: 
        #print("Variable: ", var[0], "Expresión regular: ", var[1])

        # Analizando cada expresión regular para ver que sea consistente.
        bool, expres = deteccion2(var[1])

        # Buscando en que línea del archivo está la regex que pudo tener error.
        if bool == "Corchetes": 
            #print("Expresión regular: ", expres)
            #print("Línea: ", data.find(expres))
            # Imprimiendo también la posición del error.
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " hay corchetes desbalanceados en la regex")
            
        
        if bool == "Parent":
            #print("Expresión regular: ", expres)
            #print("Línea: ", data.find(expres))
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " hay paréntesis desbalanceados en la regex")
        
        if bool == "BB":
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " la regex empieza con un * o un +.")
        
        if bool == "OF":
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " la regex finaliza con un |.")
        


        # Revisando que las declaraciones de variables estén bien escritas.

        # Imprimiendo las declaraciones.
        #print(var[0])

        bool, expres = deteccion2(var[0])
        
        if bool == "Corchetes":
            #print("Expresión regular: ", expres)
            #print("Línea: ", data.find(expres))
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " hay corchetes desbalanceados en la variable")
        
        if bool == "Parent":
            #print("Expresión regular: ", expres)
            #print("Línea: ", data.find(expres))
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " hay paréntesis desbalanceados en la variable")
        
        if bool == False: 
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " la variable solo debe tener letras o números")
        
        if bool == "BB":
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " la regex empieza con un * o un +.")
        
        if bool == "OF":
            print("Error en la línea: ", data.count('\n', 0, data.find(expres)), " la regex finaliza con un |.")
    
    # Jalando los tokens especiales.
    if "rule gettoken =" in data:
        # Extrayendo la cadena de texto que contiene los tokens especiales.
        cadena_tokens = data[data.find("rule gettoken ="):]
        # Separando los tokens en una lista.
        lista_tokens = cadena_tokens.split("|")
        # Creando el diccionario para guardar los tokens.
        diccionario_tokens = {}
        # Iterando sobre la lista de tokens y agregándolos al diccionario.
        for token in lista_tokens:
            # Extrayendo el nombre del token y su valor.
            nombre, valor = token.split("return")
            # Agregando el token al diccionario.
            diccionario_tokens[nombre.strip()] = valor.strip().strip("\"")
        # Imprimiendo el diccionario con los tokens.
        #print(diccionario_tokens)

        # Detectando las palabras reservadas.

        # Crear un nuevo diccionario sin la cadena deseada.
        nuevo_diccionario = {}
        for clave, valor in diccionario_tokens.items():
            clave_limpia = clave.replace('rule gettoken = \n', "").strip()
            nuevo_diccionario[clave_limpia] = valor

        # Imprimir el nuevo diccionario sin la cadena.
        # print(nuevo_diccionario)

        # Ordenando el diccionario.
        diccionario_ordenado = dict(sorted(nuevo_diccionario.items()))
        #print("Diccionario ordenado: ", diccionario_ordenado)

        lista_temp = []

        for clave in diccionario_ordenado.keys():
            palabra = clave.replace('{', '').strip()
            lista_temp.append(palabra)
        
        #print(lista_temp)

        for elemento in lista_temp:
            elemento_sin_comillas = elemento.replace('"', "")
            res_list.append(elemento_sin_comillas)
        
        # Detectando los operadores aritméticos del gettoken.
        operadores = ["*", "^", "+", "-", "/", "(", ")"]

        # Lista para los operadores reservados.
        operadores_reservados = []

        # Operadores reservados.
        for elemento in res_list:
            #print("Elemento: ", elemento)
            if elemento in operadores:
                operadores_reservados.append(elemento)

        print("Operadores resrvados: ", operadores_reservados)

        # Sacando los operadores de la lista de palabras reservadas.
        for elemento in operadores_reservados:
            res_list.remove(elemento)

        # Resto de tokens.
        tokens = [] # Lista para guardar los tokens.
        for elemento in res_list:
            tokens.append(elemento)
        
        # Limpiando la lista.
        res_list.clear()


    #print(res_list)

    # Almacenando el nombre de las variables y su expresión regular en la tabla.
    for variable in variables:
        tabla[variable[0]] = variable[1]
    
    #print("Tabla al principio: ", tabla)
    
    # Reemplazando el E por un epsilon.
    for key in tabla:
        tabla[key] = tabla[key].replace("E", "ε")
    
    #print("Tabla: ", tabla)

    # Reemplazos.

    # Letras.
    # Verificando que sí haya una definición de letras.
    if 'letter' in tabla:
        new_letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
        tabla['letter'] = tabla['letter'].replace("['a'-'z' 'A'-'Z']", new_letters)
        #print("Tabla: ", tabla)

    # Números.
    # Verificando que sí haya una definición de números.
    if 'digit' in tabla:
        new_digits = '(0|1|2|3|4|5|6|7|8|9)'
        tabla['digit'] = tabla['digit'].replace("['0'-'9']", new_digits)
    
    
    # Verificando si hay una definición de digit+
    if 'digits' in tabla:
        new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
        tabla['digits'] = tabla['digits'].replace("digit+", new_digitsp)
    
    # Verificando si hay una definición de space.
    if 'space' in tabla: 
        new_space = '(_)(_)*'
        tabla['space'] = tabla['space'].replace("space", new_space)
    
    # Verificando si hay una definición de endline.
    if 'endline' in tabla:
        new_endline = '(xyz)(xyz)*'
        tabla['endline'] = tabla['endline'].replace("endline", new_endline)
    
    #print("Tabla: ", tabla)

    # Verificando si hay una definición id.
    if 'id' in tabla:
        new_letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
        new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
        new_space = '(_)(_)*'
        new_endline = '(xyz)(xyz)*'
        """
            El reemplazo sería:
            id = (letter(letter|digits|space)*)endline
            en donde letter se cambia por new1_letters, 
            digits por new_digitsp, space por new_space,
            y endline por new_endline.
        """

        tabla['id'] = tabla['id'].replace("letter", new_letters)
        tabla['id'] = tabla['id'].replace("digits", new_digitsp)
        tabla['id'] = tabla['id'].replace("space", new_space)
        tabla['id'] = tabla['id'].replace("endline", new_endline)
        
    #print("Tabla: ", tabla)

    # Verificando si hay una definición de number.
    if 'number' in tabla:
        new_digitsp = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
        new_signs = "(@|~)"
        """
            El reemplazo sería:
            digits se cambia por new_digitsp.
        """

        tabla['number'] = tabla['number'].replace("digits", new_digitsp)
        tabla['number'] = tabla['number'].replace("sign", new_signs)
    
    if 'sign' in tabla: 
        new_signs = "(@|~)"
        tabla['sign'] = tabla['sign'].replace("['+'|'-']", new_signs)
    
    # Leyendo el delim.
    if 'delim' in tabla:

        #print("Hay un delim")

        new_delims = "(≡|¥|§)"
        tabla['delim'] = tabla['delim'].replace("[' ''\\t''\\n']", new_delims)
    
    if 'ws' in tabla: 
        new_delimsp = "(≡|¥|§)(≡|¥|§)*"
        tabla['ws'] = tabla['ws'].replace("delim+", new_delimsp)

        # Verificando como está el delim.
        # Si el delim está así [' ''\t''\n'], crear un or entre ellos.
        # Verificando si se hizo el cambio.
        #print("Tabla: ", tabla)
    
    if 'letterh' in tabla: 
        new_letters_h = '(A|B|C|D|E|F)'
        tabla['letterh'] = tabla['letterh'].replace("['A'-'F']", new_letters_h)
    
    if 'lettersh' in tabla: 
        new_letters_hs = '(A|B|C|D|E|F)(A|B|C|D|E|F)*'
        tabla['lettersh'] = tabla['lettersh'].replace("letterh+", new_letters_hs)
    
    if 'digite' in tabla: 
        new_digits_e = '(0|1|2|3|4|5|6|7|8|9)'
        tabla['digite'] = tabla['digite'].replace("['0'-'9']", new_digits_e)
    
    if 'digitse' in tabla: 
        new_digitsp_e = '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'
        tabla['digitse'] = tabla['digitse'].replace("digite+", new_digitsp_e)
    
    # Buscando los hexdigit.
    if 'hexdigit' in tabla:
        new_letters_h = '(A|B|C|D|E|F)'
        new_digits_e = '(0|1|2|3|4|5|6|7|8|9)'

        tabla['hexdigit'] = tabla['hexdigit'].replace("letterh", new_letters_h)
        tabla['hexdigit'] = tabla['hexdigit'].replace("digitse", new_digits_e)
    
    # Buscando los strings.
    if 'string' in tabla:
        new_letter = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)"
        new_digit = "(0|1|2|3|4|5|6|7|8|9)"
        new_space = "(_)"

        # Uniendo las cosas para hacer la cerradura positiva.
        new_all = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9)|( )(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9)|( )*"

        tabla['string'] = tabla['string'].replace("(letter|digito| )+", new_all)


    # Verificando si existen corchetes para reemplazarlos con paréntesis.
    for key in tabla:
        tabla[key] = tabla[key].replace("[", "(")
        tabla[key] = tabla[key].replace("]", ")")

    #print("Tabla: ", tabla)

    # Metiendo a una lista los valores del diccionario.
    listaA = []

    listaF = []

    for key in tabla:
        listaA.append(tabla[key])
    
    #print("Lista: ", lista)
    regex_final = ""
    alf_final = ""
    lista_temp = []
    lista_diccionarios = [] # Este va a tener los diccionarios de cada AFD.
    lista_iniciales = [] # Este va a tener los estados iniciales de cada AFD.
    lista_finales = [] # Este va a tener los estados finales de cada AFD.


    for i in range(len(listaA)):
        regex = listaA[i]
        regex = regex.replace("?", "|ε")

        if "*" in regex:
            regex = regex.replace("*****************", "*")
            regex = regex.replace("****************", "*")
            regex = regex.replace("***************", "*")
            regex = regex.replace("**************", "*")
            regex = regex.replace("************", "*")
            regex = regex.replace("**********", "*")
            regex = regex.replace("********", "*")
            regex = regex.replace("******", "*")
            regex = regex.replace("*****", "*")
            regex = regex.replace("****", "*")
            regex = regex.replace("***", "*")
            regex = regex.replace("**", "*")

        regex = regex.replace("'", "")
        listaA[i] = regex

        # Verificando que la expresión esté bien.
        bien = deteccion(regex)

        if bien: 

            # Obteniendo individualmente cada alfabeto.
            alfI = alfabeto(regex)

            # Pasando individualmente cada expresión a postfix.
            regexI = evaluar(regex)

            #print("RegexI: ", regexI)

            # Creando el AFD temporal.
            arbol = SintaxT(regexI, alfI)

            # Guardando los datos de cada AFD.

            lista_diccionarios.append(arbol.dict) 

            lista_iniciales.append([arbol.EstadoInicial])

            lista_finales.append(arbol.EstadosAceptAFD)

        else: 
            print("Hubo un error con la regex")


    # #print("ListaA: ", listaA)

    # Uniendo todas las expresiones mediante un |.
    expr = "|".join(listaA)

    print("Expresión unida: ", expr)

    reg = evaluar(expr)

    # Verificando que la expresión regular no tenga errores.
    bien = deteccion(expr)

    if bien:
    
        # Pasando a postfix.
        regex_final = evaluar(expr)

        #print("Expresión unida en postfix: ", regex_final)

        # Obteniendo alfabeto.
        alf_final = alfabeto(regex_final)

        #SintaxT(regex_final, alf_final)
    
    else: 
        print("Hubo un error con la regex")

    # print("Lista de diccionarios: ", lista_diccionarios)

    # print("Lista de iniciales: ", lista_iniciales)

    # print("Lista de finales: ", lista_finales)

    new_w = " " # Quitando el ≡ de los diccionarios.

    for dictionary in lista_diccionarios:
        for key in dictionary:
            if "≡" in dictionary[key]:
                value = dictionary[key].pop("≡")
                dictionary[key][new_w] = value
    
    # Quitando el ¥ de los diccionarios.
    new_t = "\t"
    for dictionary in lista_diccionarios:
        for key in dictionary:
            if "¥" in dictionary[key]:
                value = dictionary[key].pop("¥")
                dictionary[key][new_t] = value
    
    # Quitando el ¥ de los diccionarios.
    new_n = "\n"
    for dictionary in lista_diccionarios:
        for key in dictionary:
            if "§" in dictionary[key]:
                value = dictionary[key].pop("§")
                dictionary[key][new_n] = value
    
    # Quitando el @ de los diccionarios.
    new_p = "+"
    for dictionary in lista_diccionarios:
        for key in dictionary:
            if "@" in dictionary[key]:
                value = dictionary[key].pop("@")
                dictionary[key][new_p] = value
    
    # Quitando el ~ de los diccionarios.
    new_m = "-"
    for dictionary in lista_diccionarios:
        for key in dictionary:
            if "~" in dictionary[key]:
                value = dictionary[key].pop("~")
                dictionary[key][new_m] = value

    # Si se quiere ver el árbol, descomentar la línea 227 del SintaxTree.


    # Llamando al simulador del txt.
    SimuladorTxT(lista_diccionarios, lista_iniciales, lista_finales, archivo, res_list, operadores_reservados, tokens, tabla)


# Probando compilar un archivo yalex.
