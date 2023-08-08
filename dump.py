# Función para generar el listado de conexiones con formato ngPAWS
def formatea_conexiones(listConnections, num_locations, contador_aContainer_true, listRooms):
    dest_map = {}
    for item in listConnections:
        dest_map.setdefault(int(item['locini']), []).append((item['direccion'], int(item['locdest'])))

    formatted_text = ""
    
    for i in range(num_locations):
        formatted_text += f'/{i}\n'
        for direccion, locdest in dest_map.get(i, []):
            localidad_destino = locdest + contador_aContainer_true - 1
            destino = listRooms[localidad_destino]['name']
            formatted_text += f' {direccion} \t{locdest + contador_aContainer_true} \t;{destino}\n'

        print("PASO " + str(i))
        print(formatted_text)

    return formatted_text


contador_aContainer_true = 2

# Ejemplo de datos simulados
listConnections = [
    {'locini': '0', 'direccion': 'ABAJO', 'locdest': '9'},
    {'locini': '0', 'direccion': 'ARRIBA', 'locdest': '8'},
    # ... otros elementos de la lista
]

listRooms = [
    {'name': 'Cave NORTE (2)'},
    {'name': 'Cave (1)'},
    {'name': 'Cave (1)'},
    {'name': 'Cave (1)'},
    # ... otros elementos de la lista
]

num_locations = 4  # El número total de ubicaciones

resultado = formatea_conexiones(listConnections, num_locations, contador_aContainer_true, listRooms)
print(resultado)