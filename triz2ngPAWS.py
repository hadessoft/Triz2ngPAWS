#! python

###########################################
#        Triz2ngPAWS by Tranqui69         #
#      Club de Aventuras AD (CAAD)        #
#           https://caad.club             @
###########################################

import re
import sys
import xml.etree.ElementTree as ET
import json
from unidecode import unidecode

###########################################
### Sección de declaración de variables ###
###########################################

localidades = []
objetos  = []
conexiones = []
LOCVAR = ""
OBJVAR = ""
OBJNAMES = ""
OBJETOS = ""

# Rosa de los vientos con los puntos cardinales y las direcciones básicas.
rosa_vientos = {
    'n': 'NORTE', 's': 'SUR', 'e': 'ESTE', 'w': 'OESTE',
    'ne': 'NORESTE', 'nw': 'NOROESTE', 'se': 'SURESTE', 'sw': 'SUROESTE',
    'up': 'ARRIBA', 'down': 'ABAJO', 'in': 'ENTRAR', 'out': 'SALIR'
}

###########################################
### Sección de declaración de funciones ###
###########################################

###########################################
#### Funciones Trizbort                 ###
###########################################

# Función para extraer los objetos
def buscar_objetos(root):
    global objetos

    for room in root.findall('.//room'):
        room_id = room.get('id')  # Obtener el valor del atributo 'id' de la etiqueta 'room'
        objects_element = room.find('objects')
        if objects_element is not None:
            objects_text = objects_element.text
            if objects_text:  # Comprobamos que el atributo no este vacío
                objetos_individuales = objects_text.split('|')
                for objeto_individual in objetos_individuales:
                    # Utilizamos expresiones regulares para buscar marcadores en el objeto individual
                    obj_name = re.sub(r'\[.*?\]', '', objeto_individual)  # Eliminamos los corchetes
                    obj_name = obj_name.strip()  # Eliminamos espacios en blanco
                   
                    obj_data = {
                        'name': obj_name,  # Guardamos el nombre del objeto individual
                        'loc': int(room_id),
                        'weight': 1,
                        'aLight': False,
                        'aWear': False,
                        'aMale': False,
                        'aFemale': False,
                        'aContainer': False,
                        'aNPC': False,
                        'aNeuter': False,
                        'aPlural': False,
                        'aScenery': False,
                        'aConcealed': False,
                        'aStatic': False,
                        'aEdible': False,
                        'aDrinkable': False,
                        'aEnterable': False,
                        'aOpen': False,
                        'aOpenable': False,
                        'aLockable': False,
                        'aLocked': False,
                        'aTransparent': False,
                        'aSwitchable': False,
                        'aOn': False,
                        'aSupporter': False,
                        'content': [],
                    }

                    # Aplicamos las condiciones según los marcadores en el objeto individual
                    if '[c]' in objeto_individual:
                        obj_data['aContainer'] = True
                    if '[l]' in objeto_individual:
                        obj_data['aLight'] = True
                    if '[f]' in objeto_individual:
                        obj_data['aFemale'] = True
                    if '[m]' in objeto_individual:
                        obj_data['aMale'] = True
                    if '[w]' in objeto_individual:
                        obj_data['aWear'] = True
                    if '[n]' in objeto_individual:
                        obj_data['aNeuter'] = True
                    if '[s]' in objeto_individual:
                        obj_data['aScenery'] = True
                    if '[u]' in objeto_individual:
                        obj_data['aSupporter'] = True

                    objetos.append(obj_data)
                  
        # Ordenamos los objetos para poner los contenedores al principio            
        objetos = sorted(objetos, key=lambda x: (not x['aContainer'], x['name']))

        # Recorremos y asignamos un índice secuencial a cada objeto
        for index, objeto in enumerate(objetos):
            objeto['id'] = index

    return objetos

# Función que devuelve el número de objetos con la propiedad 'aContainer'
def buscar_contenedores(data):
    # Contador para llevar la cuenta de los elementos con aContainer en true
    contador_aContainer_true = 0

    for item in data:
        if item["aContainer"]:
            contador_aContainer_true += 1

    return contador_aContainer_true

# Función para extraer las localidades
def buscar_localidades(contador_contenedores, root):

    num_localidades_totales = len(root.findall('.//room')[:-1]) + contador_contenedores

    localidades = []

    for loc in range(num_localidades_totales):
        if loc < contador_contenedores:
            # Generar localidades adicionales
            room_data = {
                'name': f'Location {loc}',
                'subtitle': '',
                'description': f'Objeto Contenedor {loc}',
                'loc': loc,
                'id': '',
                'objects': [],
                'exits': []
            }
            localidades.append(room_data)
        else:
            # Obtener localidades desde root.findall('.//room')[:-1]
            room = root.findall('.//room')[loc - contador_contenedores]
            objects_element = room.find('objects')
            if objects_element is not None and objects_element.text is not None:
                objects = [obj.strip() for obj in objects_element.text.split('|') if obj.strip()]
            else:
                objects = []

            room_data = {
                'name': room.get('name', f'Location {loc}'),
                'subtitle': room.get('subtitle', ''),
                'description': room.get('description', f'Description of Location {loc}'),
                'loc': loc,
                'id': room.get('id', ''),
                'objects': objects,
                'exits': []
            }
            localidades.append(room_data)

    localidades = sorted(localidades, key=lambda x: x['loc'])
    return localidades

def buscar_conexiones(root):
    # Convertir las líneas en un formato JSON
    lines_json = []
    global conexiones
    
    for line in root.findall('.//line'):
        line_data = {
            'id': line.get('id'),
            'name': line.get('name'),
            'description': line.get('description'),
            'startText': line.get('startText'),
            'endText': line.get('endText'),
            'flow': line.get('flow'),
            'docks': [
                {'index': dock.get('index'), 'id': dock.get('id'), 'port': dock.get('port')}
                for dock in line.findall('dock')
            ]
        }

        if line_data['id'] is not None and 'docks' in line_data and line_data['docks']:
            if line_data['flow'] == 'oneWay':
                # Se trata de un camino de solo ida
                if line_data['docks'][0]['port'] not in rosa_vientos:
                    line_data['docks'][0]['port'] = line_data['startText']
                else: 
                    line_data['docks'][0]['port'] = line_data['docks'][0]['port']
                direction_ida = rosa_vientos.get(line_data['docks'][0]['port'], line_data['docks'][0]['port'])
                datos_conexion = {
                    'locini': line_data['docks'][0]['id'],               
                    'direccion': direction_ida,
                    'locdest': line_data['docks'][1]['id'],
                }
                conexiones.append(datos_conexion)                
            else:
                # Al ser de ida y vuelta hay que generar los dos valores
                if line_data['docks'][0]['port'] not in rosa_vientos:
                    line_data['docks'][0]['port'] = line_data['startText']
                    line_data['docks'][1]['port'] = line_data['endText']
                else: 
                    line_data['docks'][0]['port'] = line_data['docks'][0]['port']

                direction_ida = rosa_vientos.get(line_data['docks'][0]['port'], line_data['docks'][0]['port'])
                direction_vuelta = rosa_vientos.get(line_data['docks'][1]['port'], line_data['docks'][1]['port'])
                datos_conexion = {
                    'locini': line_data['docks'][0]['id'],               
                    'direccion': direction_ida,
                    'locdest': line_data['docks'][1]['id'],
                }
                conexiones.append(datos_conexion)
                #Generamos la conexion de vuelta
                datos_conexion = {
                    'locini': line_data['docks'][1]['id'],               
                    'direccion': direction_vuelta,
                    'locdest': line_data['docks'][0]['id'],
                }
                conexiones.append(datos_conexion)
                
    # Ordenamos el array
    conexiones = sorted(conexiones, key=lambda x: (x['locini'], x['direccion']))    
    return conexiones

def procesar_salidas(conexiones, localidades):
    for item in conexiones:
        locini = buscar_loc_por_id(localidades, item['locini'])
        locdest = buscar_loc_por_id(localidades, item['locdest'])
        item['locini'] = locini
        item['locdest'] = locdest
        
        localidades[locini]['exits'].append(item['direccion'] + ' '+str(locdest))
    
    conexiones = sorted(conexiones, key=lambda x: (x['locini'], x['direccion']))        
    return conexiones

def procesar_objetos(objetos):
    for item in objetos:
        locini = buscar_loc_por_id(localidades, item['loc'])
        item['loc'] = locini
            
    return objetos

###########################################
### Funciones auxiliares                ###
###########################################

# Imprime un array como json
def print_as_json(data):
    formatted_json = json.dumps(data, indent=4)
    print(formatted_json)

def eliminar_acentos(texto):
    texto_sin_acentos = unidecode(texto)
    return texto_sin_acentos

# Permite buscar una localidad por su id y devuelve el número real
def buscar_loc_por_id(localidades, id_buscado):
    for item in localidades:
        if str(item.get('id')) == str(id_buscado):
            return item.get('loc')
    return None

# Función para generar las variables de objetos y localidades
def generaVariable(input_line, tipo):
    # Eliminar números y espacios alrededor
    cleaned_line = re.sub(r'\(\d+\)', '', input_line).strip()
    
    # Convertir a minúsculas y eliminar espacios
    words = cleaned_line.split()
    processed_words = [ word.capitalize() for word in words]
    processed_line = ''.join(processed_words)
    
    return tipo+processed_line

def genera_flags():
    VARIABLES = ""
    with open("inc/VAR.txt", 'r', encoding='utf-8') as header_file:
        VARIABLES = header_file.read()
        VARIABLES = VARIABLES.replace(";Variables_de_Localidades", LOCVAR)
        VARIABLES = VARIABLES.replace(";Variables_de_Objetos", OBJVAR)
    return VARIABLES

def genera_vocabulario():
    VOCABULARIO = "/VOC\n"
    for header_filename in ["inc/DIR.txt", "inc/NOM.txt", "inc/VER.txt", "inc/ADJ.txt",  "inc/ADV.txt", "inc/PRE.txt", "inc/PNM.txt", "inc/CNJ.txt"]:
        with open(header_filename, 'r', encoding='utf-8') as header_file:
            VOCABULARIO += header_file.read() + "\n"
    return VOCABULARIO

def genera_tabla_procesos():
    PROCESOS = ""
    for header_filename in ["inc/PRO0.txt", "inc/PRO1.txt", "inc/PRO2.txt"]:
        with open(header_filename, 'r', encoding='utf-8') as header_file:
            PROCESOS += header_file.read() + "\n"
    return PROCESOS

def genera_sysmes():
    SYSMES = ""
    with open("inc/STX.txt", 'r', encoding='utf-8') as header_file:
        SYSMES += header_file.read() 
    return SYSMES

def genera_usrmes():
    USRMES = ""
    with open("inc/MTX.txt", 'r', encoding='utf-8') as header_file:
        USRMES += header_file.read() 
    return USRMES

def genera_conexiones():
    CON = "/CON\n"
    CON += "; Ejemplo\n"
    CON += "; N\t4\n"
    CON += "; E\t2\n"

    for room in localidades:
        CON += "/"+ str(room['loc'])+"\t\t ; "+str(room['name'])+"\n"
        # Unir los elementos del array con saltos de línea        
        CON += "\n".join(room['exits']) + "\n"
    return CON

def genera_localidades():    
    global LOCVAR
    LOCALIDADES = "/LTX\n"    
    contador = 0

    # Generamos las localidades
    for room in localidades:        
        LOCALIDADES += '/' + str(room['loc']) + "\n"
        LOCALIDADES += room['description'] + "\n"

        loc_definition = generaVariable(eliminar_acentos(room['name']), '#define loc l')
        if loc_definition in LOCVAR:
            contador += 1
            LOCVAR += generaVariable(eliminar_acentos(room['name']), '#define loc l') + str(contador) + '\t' + str(room['loc']) + "\n"
        else:
            LOCVAR += generaVariable(eliminar_acentos(room['name']), '#define loc l') + '\t' + str(room['loc']) + "\n"

    return LOCALIDADES

def genera_objetos():    
    global OBJVAR, OBJNAMES, OBJETOS

    OBJETOS = "/OBJ\n"
    OBJETOS += ";obj\tloc\t\tpeso\tnombre\t\tadjetivo\t\tatributo\n"
    OBJETOS += ";num\tini\n"

    # Generamos los objetos
    obj_index = 0
    for obj in objetos:
        attributes = ' '.join([attr for attr, value in obj.items() if value and attr.startswith('a')])
        OBJETOS += f"/{obj_index}\t \t{obj['loc']-1}\t \t{obj['weight']}\t \t{eliminar_acentos(obj['name']).upper()}\t\t_\t\tATTR {attributes}\n"
        OBJNAMES += f"/{obj_index}\n{obj['name'].upper()}\n"
        OBJVAR += generaVariable(eliminar_acentos(obj['name']), '#define obj o') + '\t' + str(obj_index) + "\n"
        obj_index += 1
    return OBJETOS


## Inicio del proceso
print('**********************************************************')
print('* Triz2ngPAWS versión 0.0.2b13 230809 (c) 2023 Tranqui69 *')     
print('**********************************************************')

# Comprobamos que se pase como parámetro un archivo con la extensión .trizbort
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ayuda: py triz2ngPAWS.py archivo.trizbort")
        sys.exit(1)   
    filename = sys.argv[1]
    
# Cargamos el archivo XML
tree = ET.parse(filename)
root = tree.getroot()

# Contamos el número de objetos contenedores definidos.
# En ngPAWS habrá que reservar 'x' localidades para esos contenedores
print('- Buscando objetos...')
objetos = buscar_objetos(root)
print(f'    Objetos totales encontrados  : {len(objetos)}')
num_contenedores = buscar_contenedores(objetos)  
print(f'            [{num_contenedores} son contenedores]')

# Extraemos la información de las localidades y la almacenamos en el array
# Añadiremos localides vacías para hacer hueco a los contenedores
print('- Buscando localidades...')
localidades = buscar_localidades(num_contenedores, root)
print(f'    Localidades encontradas     : {len(localidades)-num_contenedores}')
print(f'            [más {num_contenedores} que son contenedores]')

print('- Buscando conexiones...')
conexiones = buscar_conexiones(root)

# Ajustamos los valores de las localidades para tener en cuenta los contenedores
print('- Procesando objetos y localidades...')
conexiones = procesar_salidas(conexiones, localidades)
objetos = procesar_objetos(objetos)

# Comenzamos a generar la Base de Datos de inicio

###########################################
### Créditos y cabecera                ###
###########################################

CABECERA = ""
with open("inc/HEAD.txt", 'r', encoding='utf-8') as header_file:
    CABECERA = header_file.read()

###########################################
### Definición de secciones             ###
###########################################

genera_objetos()

CTL = "" # Control (Deshuso)

VOC = genera_vocabulario() # Vocabulario

STX = genera_sysmes() # Mensajes del sistema

MTX = genera_usrmes() # Mensajes del usuario


LTX = genera_localidades() # Descripción de las localidades

CON = genera_conexiones() # Lista de conexiones

OBJ = OBJETOS # Propiedades de los objetos.

OTX = OBJNAMES # Descripción de los objetos

PRO = genera_tabla_procesos() # Tabla de procesos

VAR = genera_flags() # Flags y Variables


###########################################
### Exportamos el archivo TXP           ###
###########################################

output_filename = filename.rsplit('.', 1)[0] + '.txp'
with open(output_filename, 'w', encoding='utf-8') as output_file:
    
    print(CABECERA, file=output_file)
    print(VAR, file=output_file)
    print(VOC, file=output_file)
    print(STX, file=output_file)
    print(MTX, file=output_file)
    print(OTX, file=output_file)
    print(LTX, file=output_file)
    print(CON, file=output_file)
    print(OBJ, file=output_file)
    print(PRO, file=output_file)

    print('ÉXITO: Fichero generado correctamente')


