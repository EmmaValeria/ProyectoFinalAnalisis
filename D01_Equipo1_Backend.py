import math
import copy

type Ubicacion = tuple[float, float]

class NodoUbicacion:
    def __init__(self, peso: int, ubicacion: Ubicacion, anterior: object, siguiente: object) -> None:
        self.peso = peso
        self.ubicacion = ubicacion
        self.anterior = anterior
        self.siguiente = siguiente
    
    def set_anterior(self, anterior: object) -> None:
        self.anterior = anterior
    
    def set_siguiente(self, siguiente: object) -> None:
        self.siguiente = siguiente

type Ruta = list[NodoUbicacion]

def distancia_euclidiana(u1: Ubicacion, u2: Ubicacion) -> float:
    distancia = math.sqrt((u2[0] - u1[0])**2 + (u2[1] - u1[1])**2)
    return distancia

def matriz(ubicaciones: tuple) -> list:
    matriz = []
    for i in ubicaciones:
        fila = []
        for j in ubicaciones:
            distancia = distancia_euclidiana(i, j)
            fila.append(distancia)
        matriz.append(fila)
    return matriz

def tabla_de_ahorros(distancias: list) -> dict[tuple[int, int], float]:
    tabla = {}
    for fila in range(len(distancias)):
        if fila == 0: continue
        for columna in range(len(distancias[fila])):
            if columna <= fila: continue
            indice_ubicaciones = (fila, columna)
            tabla[indice_ubicaciones] = distancias[0][fila] + distancias[0][columna] - distancias[fila][columna]
    return tabla

def ubicaciones_a_nodos(ubicaciones: tuple) -> list[NodoUbicacion]:
    paquetes = []
    peso = 1
    for ubicacion in ubicaciones:
        paquete = NodoUbicacion(peso, ubicacion, None, None)
        paquetes.append(paquete)
    return paquetes

def añadir_a_ruta(ruta: Ruta, max_peso: int, peso: int, ubicacion: NodoUbicacion, posicion: bool) -> int:
    if len(ruta) == 0: ubicacion_copia = copy.deepcopy(ubicacion); ruta.append(ubicacion_copia); return peso
    if posicion:
        ubicacion.set_anterior(ruta[0])
        try:
            ubicacion.set_siguiente(ruta[1])
            ruta[1].set_anterior(ubicacion)
        except IndexError:
            ubicacion.set_siguiente(ruta[0])
        ruta.insert(1, ubicacion)
        peso += 1
        return peso
    else:
        ubicacion.set_siguiente(ruta[0])
        ubicacion.set_anterior(ruta[-1])
        ruta[-1].set_siguiente(ubicacion)
        ruta.append(ubicacion)
        peso += 1
        return peso

def seleccion_ruta(ruta_1: Ruta, ruta_2: Ruta, ubicaciones: list[NodoUbicacion], posibles_rutas: tuple[int, int], peso_max_1: int, peso_max_2: int, peso_1: int, peso_2: int) -> tuple[int, int] | None:
    def añadir_ruta_1(ruta_1: Ruta, ubicaciones_colindantes: list[NodoUbicacion], ubicacion_posible_1: NodoUbicacion, ubicacion_posible_2: NodoUbicacion, peso_max_1: int, peso_1: int, peso_2: int) -> tuple[int, int]:
        if ubicacion_posible_1 in ubicaciones_colindantes:
            if ubicacion_posible_1 == ubicaciones_colindantes[0]: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_2, True); return (peso_1, peso_2)
            else: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_2, False); return (peso_1, peso_2)
        else:
            if ubicacion_posible_2 == ubicaciones_colindantes[0]: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_1, True); return (peso_1, peso_2)
            else: peso_1 = añadir_a_ruta(ruta_1, peso_max_1, peso_1, ubicacion_posible_1, False); return (peso_1, peso_2)
    def añadir_ruta_2(ruta_2: Ruta, ubicaciones_colindantes: list[NodoUbicacion], ubicacion_posible_1: NodoUbicacion, ubicacion_posible_2: NodoUbicacion, peso_max_2: int, peso_1: int, peso_2: int) -> tuple[int, int]:
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
        if (ubicacion_posible_1 in ruta_1 or ubicacion_posible_2 in ruta_1) and (peso_1 + 1) <= peso_max_1: # Si una de las posibles direcciones ya esta en ruta 1.
            ubicaciones_colindantes = [ruta_1[1], ruta_1[-1]]
            pesos = añadir_ruta_1(ruta_1, ubicaciones_colindantes, ubicacion_posible_1, ubicacion_posible_2, peso_max_1, peso_1, peso_2)
            return pesos
        else: # Si ninguna de las dos esta en la ruta 1
            peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_1, True)
            peso_2 = añadir_a_ruta(ruta_2, peso_max_2, peso_2, ubicacion_posible_2, True)
            return (peso_1, peso_2)
    else:
        ubicaciones_colindantes = [ruta_1[1], ruta_1[-1], ruta_2[1], ruta_2[-1]]
        if (ubicacion_posible_1 or ubicacion_posible_2) in ubicaciones_colindantes:
            if ((peso_2 + 1) <= peso_max_2 and (ubicacion_posible_1 in ubicaciones_colindantes[2::] or ubicacion_posible_2 in ubicaciones_colindantes[2::])) and ((peso_1 + 1) <= peso_max_1 and (ubicacion_posible_1 in ubicaciones_colindantes[0:2] or ubicacion_posible_2 in ubicaciones_colindantes[0:2])):
                if len(ruta_1) <= len(ruta_2):
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

def algoritmo(peso_max_camion_1: int, peso_max_camion_2: int, *args: Ubicacion) -> list[tuple[Ruta, int]]:
    rutas = []
    ruta_1: Ruta = []
    ruta_2: Ruta = []
    peso_1 = 0
    peso_2 = 0
    matriz_distancias = matriz(args)
    ahorros = tabla_de_ahorros(matriz_distancias)
    nodos_ubicacion = ubicaciones_a_nodos(args)
    peso_1 = añadir_a_ruta(ruta_1, peso_max_camion_1, peso_1, nodos_ubicacion[0], True)
    peso_2 = añadir_a_ruta(ruta_2, peso_max_camion_2, peso_2, nodos_ubicacion[0], True)
    if len(ahorros) == 0:
        peso_1 = añadir_a_ruta(ruta_1, peso_max_camion_1, peso_1, nodos_ubicacion[1], True)
        ruta_1[0].set_siguiente(ruta_1[1])
        ruta_1[0].set_anterior(ruta_1[-1])
        rutas.append((ruta_1, peso_1))
        rutas.append((ruta_2, peso_2))
        return rutas
    ahorros = dict(sorted(ahorros.items(), key = lambda x:x[1], reverse = True))
    print(ahorros)
    posibles_ubicaciones = iter(ahorros)
    ubicaciones_por_visitar = nodos_ubicacion.copy()
    ubicaciones_por_visitar.remove(nodos_ubicacion[0])
    while(len(ubicaciones_por_visitar) != 0):
        indices = next(posibles_ubicaciones)
        posible_ubicacion_1 = nodos_ubicacion[indices[0]]
        posible_ubicacion_2 = nodos_ubicacion[indices[1]]
        if posible_ubicacion_1 in ubicaciones_por_visitar or posible_ubicacion_2 in ubicaciones_por_visitar:
            posible_parte_de_ruta = seleccion_ruta(ruta_1, ruta_2, nodos_ubicacion, indices, peso_max_camion_1, peso_max_camion_2, peso_1, peso_2)
            if posible_parte_de_ruta == None: continue
            else:
                if posible_ubicacion_1 in ubicaciones_por_visitar: ubicaciones_por_visitar.remove(posible_ubicacion_1)
                if posible_ubicacion_2 in ubicaciones_por_visitar: ubicaciones_por_visitar.remove(posible_ubicacion_2)
                peso_1 = posible_parte_de_ruta[0]
                peso_2 = posible_parte_de_ruta[1]
        else: continue
    ruta_1[0].set_siguiente(ruta_1[1])
    ruta_1[0].set_anterior(ruta_1[-1])
    rutas.append((ruta_1, peso_1))
    rutas.append((ruta_2, peso_2))
    return rutas

if __name__ == "__main__":
    CAMION_1 = 10
    CAMION_2 = 15

    algoritmo_backend = algoritmo(CAMION_1, CAMION_2, (3.0, 4.0), (1.0, 2.0), (8.0, 9.0), (3.5, 5.6))
    a = 0
    u = 0
    for ruta in algoritmo_backend:
        a += 1
        for ubicaciones in ruta:
            if type(ubicaciones) == type(1): continue
            for ubicacion in ubicaciones:
                if type(ubicacion.siguiente) == type(None): print(f'Ruta {a}: Ubicacion {ubicacion.ubicacion}')
                else: print(f'Ruta {a}: Ubicacion = {ubicacion.ubicacion}, Ubicacion Siguiente = {ubicacion.siguiente.ubicacion}, Ubicacion Anterior = {ubicacion.anterior.ubicacion}')
        print(f'')
