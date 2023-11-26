"""
BackEnd - Algoritmo de Rutas - Equipo 1 - Análisis de Algoritmo - D01.

El siguiente módulo presenta una solución del Problema de Enrutamiento
de Vehículos (VRP) basado en el algoritmo de Clarke & Wright, también
llamado de Ahorros, haciendo uso de Python para su codificación.

Example:
    El uso de este módulo está diseñado para ser utilizado mediante
    la exportación de la función 'algoritmo' o la función
    'algoritmo_json' (cuando se tenga un archivo JSON) y de la clase
    'NodoUbicacion' para su correcto funcionamiento.

    import NodoUbicacion
    
    import algoritmo
    rutas = algoritmo(argumentos)

    import algoritmo_json
    algoritmo_json()
    
Favor de checar la documentación respectiva de
cada función para obtener más información de su uso.

Este módulo sigue las guías presentadas por `Python Enhancement
Proposals`_ aceptadas en su documentación versión 3.12.

Docstrings basados en la Guía de Estilo de Google.

.. _Python Enhancement Proposals:
    https://docs.python.org/3/whatsnew/3.12.html
"""
import math
import copy
import json

CAMION_1 = 15
"""
Peso maximo de las ruta 1 en forma de constante.
"""
CAMION_2 = 10
"""
Peso maximo de las ruta 2 en forma de constante.
"""
ALMACEN = (20.654986912292184, -103.32528602468746)
"""
Constante de la ubicación del almacen.
"""
desde_json = False
"""
Bandera para obtener ubicaciones de archivo JSON.
"""
flag_big_o = False
"""
Bandera para realizar el analisis por Big O.
"""

type Ubicacion = tuple[float, float]

class NodoUbicacion:
    """
    Clase tipo NODO con atributos específicos de una ubicación con pesos.

    La visualización de las ubicaciones como NODOS permite la implementación
    de las rutas en forma de una estructura de lista enlazada, permitiendo
    una mayor información entre ubicaciones y próximos destinos.

    Attributes:
        peso: Un entero indicando el costo del paquete.
        ubicacion: Coordendas X e Y de la ubicación. Dos flotantes.
        anterior: Nodo Anterior de la lista enlazada. 
        siguiente: Nodo Siguiente de la lista enlazada.
    """
    def __init__(self, nombre: str, peso: int, ubicacion: Ubicacion, anterior: object, siguiente: object) -> None:
        """
        Metodo __init__ de NodoUbicacion.

        Args:
            nombre: Nombre de la ubicación.
            peso: Costo del paquete.
            ubicacion: Coordendas de la ubicación.
            anterior: Nodo Anterior. 
            siguiente: Nodo Siguiente.
        """
        self.nombre = nombre
        self.peso = peso
        self.ubicacion = ubicacion
        self.anterior = anterior
        self.siguiente = siguiente

    @property
    def nombre(self) -> str:
        """
        Soy la propiedad 'nombre'."""
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        self._nombre = nombre

    @property
    def ubicacion(self) -> Ubicacion:
        """
        Soy la propiedad 'ubicacion'.
        """
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, ubicacion: Ubicacion) -> None:
        self._ubicacion = ubicacion

    @property
    def anterior(self) -> object:
        """
        Soy la propiedad 'anterior'.
        """
        return self._anterior

    @anterior.setter
    def anterior(self, nodo_anterior: object) -> None:
        self._anterior = nodo_anterior

    @property
    def siguiente(self) -> object:
        """
        Soy la propiedad 'siguiente'.
        """
        return self._siguiente

    @siguiente.setter    
    def siguiente(self, nodo_siguiente: object) -> None:
        self._siguiente = nodo_siguiente

type Ruta = list[NodoUbicacion]

def distancia_euclidiana(u1: Ubicacion, u2: Ubicacion) -> float:
    """
    Función aritmética para obtener la distancia euclidiana.

    Regresa la distancia obtenida de las dos ubicaciones.

    Args:
        u1: Ubicación 1. En forma de una tupla de dos flotantes.
        u2: Ubicación 2. En forma de una tupla de dos flotantes.

    Returns:
        Flotante con la distancia euclidiana obtenida.
    """
    distancia = math.sqrt((u2[0] - u1[0])**2 + (u2[1] - u1[1])**2)
    return distancia

def matriz(ubicaciones: tuple) -> list:
    """
    Creación de una matriz de adyacencia.

    Crea una matriz de adyacencia automáticamente a partir de las
    coordenadas de cada ubicación y la función "distancia_euclidiana".

    Args:
        ubicaciones: Tupla de ubicaciones (en forma de tupla de dos flotantes).

    Returns:
        Matriz de adyacencia de distancias en forma de una lista anidada.
    """
    matriz = []
    for i in ubicaciones:
        fila = []
        for j in ubicaciones:
            distancia = distancia_euclidiana(i, j)
            fila.append(distancia)
        matriz.append(fila)
    return matriz

def tabla_de_ahorros(distancias: list) -> dict[tuple[int, int], float]:
    """
    Creación de una tabla de ahorros.

    Crea una tabla de lo que se ahorra por ir de ubicación a ubicación
    comparado con la distancia almacén a ubicación.

    Args:
        distancias: Matriz de adyacencia de distancias en forma de lista.

    Returns:
        Diccionario de los índices de las ubicaciones y el ahorro obtenido.
    """
    tabla = {}
    for fila in range(len(distancias)):
        if fila == 0: continue
        for columna in range(len(distancias[fila])):
            if columna <= fila: continue
            indice_ubicaciones = (fila, columna)
            tabla[indice_ubicaciones] = distancias[0][fila] + distancias[0][columna] - distancias[fila][columna]
    return tabla

def ubicaciones_a_nodos(ubicaciones: tuple) -> list[NodoUbicacion]:
    """
    Cambio del tipo de dato de las ubicaciones.

    Cambia las ubicaciones (representadas en tuplas de dos flotantes)
    a objetos de la clase NodoUbicacion.

    Args:
        ubicaciones: Tupla de ubicaciones (en forma de tupla de dos flotantes).

    Returns:
        Lista de todas las ubicaciones en forma de Nodos.
    """
    paquetes = []
    peso = 1
    if desde_json: nombres_ubicaciones, coordenadas = ubicaciones_json(); id_ubicacion = 0
    else: id_ubicacion = 1
    for ubicacion in ubicaciones:
        if ubicacion == ALMACEN:
            paquete = NodoUbicacion(f'almacen', 0, ALMACEN, None, None)
            paquetes.append(paquete)
        else:
            if desde_json:
                paquete = NodoUbicacion(f'{nombres_ubicaciones[id_ubicacion]}', peso, coordenadas[id_ubicacion], None, None)
                paquetes.append(paquete)
                id_ubicacion += 1
            else:
                paquete = NodoUbicacion(f'Ubicacion {id_ubicacion}', peso, ubicacion, None, None)
                paquetes.append(paquete)
                id_ubicacion += 1
    return paquetes

def añadir_a_ruta(ruta: Ruta, max_peso: int, peso: int, ubicacion: NodoUbicacion, posicion: bool) -> int:
    """
    Adición de una ubicación a una ruta elegida.

    Permite añadir una nueva ubicación a una ruta. Elige como almacén de
    la ruta a la primera ubicación a la que se le haya asignado. Esta
    adición solo puede realizarse como el primer destino o el último.

    Args:
        ruta: Ruta a la que se le va a añadir una ubicación.
        max_peso: Peso máximo soportado por el camión de la ruta.
        peso: Peso actual del camión.
        ubicacion: Ubicación representada en Nodo. Obtiene los atributos
            de anterior y siguiente en esta función.
        posicion: En donde se agregará la ubicación (Primero o Último).

    Returns:
        Peso actual de la ruta despues del nuevo paquete.

    Error:
        IndexError: Sucede cuando se agrega la primera ubicación, puesto
            que se busca un nodo siguiente a pesar de no contarlo.
    """
    if len(ruta) == 0: ubicacion_copia = copy.deepcopy(ubicacion); ruta.append(ubicacion_copia); return peso
    if posicion:
        ubicacion.anterior = ruta[0]
        try:
            ubicacion.siguiente = ruta[1]
            ruta[1].anterior = ubicacion
        except IndexError:
            ubicacion.siguiente = ruta[0]
        ruta.insert(1, ubicacion)
        peso += 1
        return peso
    else:
        ubicacion.siguiente = ruta[0]
        ubicacion.anterior = ruta[-1]
        ruta[-1].siguiente = ubicacion
        ruta.append(ubicacion)
        peso += 1
        return peso

def seleccion_ruta(ruta_1: Ruta, ruta_2: Ruta, ubicaciones: list[NodoUbicacion], posibles_rutas: tuple[int, int], peso_max_1: int, peso_max_2: int, peso_1: int, peso_2: int) -> tuple[int, int] | None:
    """
    Selección de la ruta a la que se le añade la nueva ubicación.

    Permite la selección de la ruta (1 o 2) a la que se le añadirá
    una ubicación nueva. Se realiza por distintos parámetros como
    saber si ambas rutas pueden realizar la adición o si esta vacía.
    Utiliza de la función "añadir_a_ruta" para añadir la ruta y
    retornar el resultado obtenido.

    Args:
        ruta_1: Ruta 1 a la que se le puede añadir una ubicación.
        ruta_2: Ruta 2 a la que se le puede añadir una ubicación.
        ubicaciones: Lista de todas las ubicaciones en forma de Nodos.
        posibles_rutas: Indices de las posibles nuevas ubicaciones. Conforme
            a la lista de ubicacion (en Nodos) completa.
        peso_max_1: Peso máximo soportado por el camión de la ruta 1.
        peso_max_2: Peso máximo soportado por el camión de la ruta 2.
        peso_1: Peso actual del camión de la ruta 1.
        peso_2: Peso actual del camión de la ruta 2.

    Returns:
        tuple[int, int]: Peso actual de ambas rutas, en enteros. Se regresa un valor nulo si la adición no es posible.
    """
    def añadir_ruta_1(ruta_1: Ruta, ubicaciones_colindantes: list[NodoUbicacion], ubicacion_posible_1: NodoUbicacion, ubicacion_posible_2: NodoUbicacion, peso_max_1: int, peso_1: int, peso_2: int) -> tuple[int, int]:
        # Se añade la ubicación a la Ruta 1
        if ubicacion_posible_1 in ubicaciones_colindantes:
            if ubicacion_posible_1 == ubicaciones_colindantes[0]: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_2, True); return (peso_1, peso_2)
            else: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_2, False); return (peso_1, peso_2)
        else:
            if ubicacion_posible_2 == ubicaciones_colindantes[0]: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_1, True); return (peso_1, peso_2)
            else: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_1, False); return (peso_1, peso_2)
    def añadir_ruta_2(ruta_2: Ruta, ubicaciones_colindantes: list[NodoUbicacion], ubicacion_posible_1: NodoUbicacion, ubicacion_posible_2: NodoUbicacion, peso_max_2: int, peso_1: int, peso_2: int) -> tuple[int, int]:
        # Se añade la ubicación a la Ruta 2
        if ubicacion_posible_1 in ubicaciones_colindantes:
            if ubicacion_posible_1 == ubicaciones_colindantes[2]: peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_2, True); return (peso_1, peso_2)
            else: peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_2, False); return (peso_1, peso_2)
        else:
            if ubicacion_posible_2 == ubicaciones_colindantes[2]: peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_1, True); return (peso_1, peso_2)
            else: peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_1, False); return (peso_1, peso_2)
    ubicacion_posible_1 = ubicaciones[posibles_rutas[0]]
    ubicacion_posible_2 = ubicaciones[posibles_rutas[1]]
    if len(ruta_1) == 1: # Si la ruta 1 esta vacia de direcciones.
        peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_1, True)
        peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_2, True)
        return (peso_1, peso_2)
    elif len(ruta_2) == 1: # Si la ruta 2 esta vacia de direcciones.
        if (ubicacion_posible_1 in ruta_1 or ubicacion_posible_2 in ruta_1): # Si una de las posibles direcciones ya esta en ruta 1.
            if (peso_1 + 1) <= peso_max_1:
                ubicaciones_colindantes = [ruta_1[1], ruta_1[-1]]
                pesos = añadir_ruta_1(ruta_1, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_1, peso_1, peso_2)
                return pesos
            else: return None
        else: # Si ninguna de las dos esta en la ruta 1
            peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_1, True)
            peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_2, True)
            return (peso_1, peso_2)
    else:
        ubicaciones_colindantes = [ruta_1[1], ruta_1[-1], ruta_2[1], ruta_2[-1]]
        if (ubicacion_posible_1 in ubicaciones_colindantes) or (ubicacion_posible_2 in ubicaciones_colindantes): # Checa si alguna de las ubicaciones es colindante
            if ((peso_2 + 1) <= peso_max_2 and (ubicacion_posible_1 in ubicaciones_colindantes[2::] or ubicacion_posible_2 in ubicaciones_colindantes[2::])) and ((peso_1 + 1) <= peso_max_1 and (ubicacion_posible_1 in ubicaciones_colindantes[0:2] or ubicacion_posible_2 in ubicaciones_colindantes[0:2])):
                # Revisa si ambas rutas pueden agregar a la otra ubicación.
                if len(ruta_1) <= len(ruta_2): # Selecciona la menor
                    pesos = añadir_ruta_1(ruta_1, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_1, peso_1, peso_2)
                    return pesos
                else:
                    pesos = añadir_ruta_2(ruta_2, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_2, peso_1, peso_2)
                    return pesos
            elif (peso_1 + 1) <= peso_max_1 and (ubicacion_posible_1 in ubicaciones_colindantes[0:2] or ubicacion_posible_2 in ubicaciones_colindantes[0:2]):
                pesos = añadir_ruta_1(ruta_1, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_1, peso_1, peso_2)
                return pesos
            elif (peso_2 + 1) <= peso_max_2:
                pesos = añadir_ruta_2(ruta_2, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_2, peso_1, peso_2)
                return pesos
            else: return None
        else: return None

def algoritmo(*args: Ubicacion) -> list[tuple[Ruta, int]] | str:
    """
    Algoritmo principal del código. Función exportable.

    Esta función desarrolla el algoritmo de Clarke & Wright de
    paso a paso, creando las variables necesarias para lograrlo y
    utilizando las demás funciones cuando se necesiten.
    

    Args:
        *args: Todas las coordenadas de las ubicaciones a conectar en el
            problema, representadas como tuplas de dos flotantes (X e Y).

    Returns:
        Lista de dos tuplas con dos tipos de datos, la ruta obtenida y su peso.
    """
    peso_max_camion_1 = CAMION_1
    peso_max_camion_2 = CAMION_2
    peso_1 = 0
    peso_2 = 0
    rutas = []
    ruta_1: Ruta = []
    ruta_2: Ruta = []
    if flag_big_o:
        coordenadas = list(zip(*args, *args))
        ubicaciones = (ALMACEN, *coordenadas)
    else:
        if len(*args) > ((peso_max_camion_1) + (peso_max_camion_2)): return f"Exceso de paquetes para las rutas. Favor de eliminar hasta obtener menos o igual {(peso_max_camion_1) + (peso_max_camion_2)}"
        ubicaciones = (ALMACEN, *args)
    matriz_distancias = matriz(ubicaciones)
    ahorros = tabla_de_ahorros(matriz_distancias)
    nodos_ubicacion = ubicaciones_a_nodos(ubicaciones)
    peso_1 = añadir_a_ruta(ruta_1, peso_max_camion_1, peso_1, nodos_ubicacion[0], True)
    peso_2 = añadir_a_ruta(ruta_2, peso_max_camion_2, peso_2, nodos_ubicacion[0], True)
    if len(ahorros) == 0:
        peso_1 = añadir_a_ruta(ruta_1, peso_max_camion_1, peso_1, nodos_ubicacion[1], True)
        ruta_1[0].siguiente = ruta_1[1]
        ruta_1[0].anterior = ruta_1[-1]
        rutas.append((ruta_1, peso_1))
        rutas.append((ruta_2, peso_2))
        return rutas
    ahorros = dict(sorted(ahorros.items(), key = lambda x:x[1], reverse = True))
    posibles_ubicaciones = list(ahorros.keys())
    ubicaciones_por_visitar = nodos_ubicacion.copy()
    ubicaciones_por_visitar.remove(nodos_ubicacion[0])
    iteracion = 0
    iteracion_faltante = None
    while(len(ubicaciones_por_visitar) != 0):
        indices = posibles_ubicaciones[iteracion]
        posible_ubicacion_1 = nodos_ubicacion[indices[0]]
        posible_ubicacion_2 = nodos_ubicacion[indices[1]]
        if posible_ubicacion_1 in ubicaciones_por_visitar or posible_ubicacion_2 in ubicaciones_por_visitar:
            posible_parte_de_ruta = seleccion_ruta(ruta_1, ruta_2, nodos_ubicacion, indices, peso_max_camion_1, peso_max_camion_2, peso_1, peso_2)
            if posible_parte_de_ruta == None:
                if iteracion_faltante == None: iteracion_faltante = iteracion
                iteracion += 1
                continue
            else:
                if posible_ubicacion_1 in ubicaciones_por_visitar: ubicaciones_por_visitar.remove(posible_ubicacion_1)
                if posible_ubicacion_2 in ubicaciones_por_visitar: ubicaciones_por_visitar.remove(posible_ubicacion_2)
                peso_1 = posible_parte_de_ruta[0]
                peso_2 = posible_parte_de_ruta[1]
                if iteracion_faltante != None: iteracion = iteracion_faltante; iteracion_faltante = None
                else: iteracion += 1
        else: iteracion += 1; continue
    ruta_1[0].siguiente = ruta_1[1]
    ruta_1[0].anterior = ruta_1[-1]
    rutas.append((ruta_1, peso_1))
    rutas.append((ruta_2, peso_2))
    return rutas

def ubicaciones_json() -> tuple[list, list]:
    """"
    Obtiene los atributos de las ubicaciones a partir de un JSON.

    Se obtiene una lista de los nombres de las ubicaciones y otro
    de las coordenadas de estas.

    Returns:
        Tupla de dos listas, una de nombres y otra de coordenadas.
    """
    nombres_ubicaciones = []
    ubicaciones = []
    with open("puntos_entrega.json", "r") as archivo:
        ubicaciones_json = json.load(archivo)
        for ubicacion in ubicaciones_json:
            nombres_ubicaciones.append(ubicacion['nombre'])
            coordenadas = ubicacion['coordenadas']
            ubicaciones.append((coordenadas['latitud'], coordenadas['longitud']))
    return nombres_ubicaciones, ubicaciones
    

def algoritmo_json() -> None:
    """
    Llamar al algoritmo a partir de un archivo JSON. Función exportable.

    Esta funcion llama al algoritmo principal con la información de las
    ubicaciones encontradas en el archivo JSON del proyecto. Guarda
    las rutas en otro archivo JSON llamado 'rutas'.
    """
    global desde_json
    desde_json = True
    id_ruta = 0
    json_rutas = {}
    pesos = []
    direcciones_ruta_1 = []
    direcciones_ruta_2 = []
    nombres_ubicaciones, ubicaciones = ubicaciones_json()
    rutas = algoritmo(*ubicaciones)
    for ruta in rutas:
        id_ruta += 1
        for ubi in ruta[0]: # type = NodoUbicacion
            if type(ubi.siguiente) == type(None): # Solo el almacen
                if id_ruta == 1:
                    direcciones_ruta_1.append({'nombre': ubi.nombre,
                                       'coordenadas': {'latitud': ubi.ubicacion[0], 'longitud':ubi.ubicacion[1]}})
                else:
                    direcciones_ruta_2.append({'nombre': ubi.nombre,
                                       'coordenadas': {'latitud': ubi.ubicacion[0], 'longitud':ubi.ubicacion[1]}})
            else:
                if id_ruta == 1:
                    direcciones_ruta_1.append({'nombre': ubi.nombre,
                                               'coordenadas': {'latitud': ubi.ubicacion[0], 'longitud':ubi.ubicacion[1]},
                                               'nombre_direccion_siguiente': ubi.siguiente.nombre,
                                               'nombre_direccion_anterior': ubi.anterior.nombre})
                else:
                    direcciones_ruta_2.append({'nombre': ubi.nombre,
                                               'coordenadas': {'latitud': ubi.ubicacion[0], 'longitud':ubi.ubicacion[1]},
                                               'nombre_direccion_siguiente': ubi.siguiente.nombre,
                                               'nombre_direccion_anterior': ubi.anterior.nombre})
        pesos.append(ruta[1])
    json_rutas[f'Ruta_1']={'direcciones': direcciones_ruta_1,
                                                 'peso': pesos[0]}
    json_rutas[f'Ruta_2']={'direcciones': direcciones_ruta_2,
                                                 'peso': pesos[1]}   
    with open("rutas.json", "w") as archivo_json:
        json.dump(json_rutas, archivo_json, indent=2)
    desde_json = False
    

if __name__ == "__main__":
#    algoritmo_json()
    import big_o

    flag_big_o = True

    positive_int_generator = lambda n: big_o.datagen.integers((CAMION_1 + CAMION_2), 0, 10000)
    best, others = big_o.big_o(algoritmo, positive_int_generator, n_repeats=100)
    print(best)
    
