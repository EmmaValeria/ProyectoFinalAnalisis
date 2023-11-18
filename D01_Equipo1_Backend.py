import math

type Ubicacion = tuple[float, float]
type Ruta = list[object]

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

def ubicaciones_a_nodos(ubicaciones: tuple) -> list[NodoUbicacion]:
    paquetes = []
    peso = 1
    for ubicacion in ubicaciones:
        paquete = NodoUbicacion(peso, ubicacion, None, None)
        paquetes.append(paquete)
    return paquetes

def seleccion_ruta(posibles_ruta_1: Ruta, posibles_ruta_2: Ruta) -> numero_ruta: int, posicion: int:
    return

def algoritmo(camion1: int, camion2: int, *args: Ubicacion) -> list[Ruta]:
    ruta_1: Ruta = []
    ruta_2: Ruta = []
    matriz_ubicaciones = matriz(args)
    nodos_ubicacion = ubicaciones_a_nodos(args)
    ubicaciones_por_visitar = nodos_ubicacion.copy()
    ubicacion = 0
    ruta_1.append(nodos_ubicacion[ubicacion])
    ruta_2.append(nodos_ubicacion[ubicacion])
    ubicaciones_por_visitar.remove(nodos_ubicacion[ubicacion])
    while(len(ubicaciones_visitadas) != 0):
        seleccion_ruta(
        ruta_1.append(nodos_ubicacion[ubicacion])
        ruta_2.append(nodos_ubicacion[ubicacion])
    return nodos_ubicacion

if __name__ == "__main__":
    CAMION_1 = 10
    CAMION_2 = 15

    algoritmo_backend = algoritmo(CAMION_1, CAMION_2, (3.0, 4.0), (1.0, 2.0))
    print(f'{algoritmo_backend}')
