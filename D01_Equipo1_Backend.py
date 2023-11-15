import math

type Ubicacion = tuple[float, float]
type Ruta = dict[str, Ubicacion]

class Node:
    def __init__(self, ubicacion=Ubicacion, left=None, right=None):
        self.ubicacion = ubicacion
        self.left = left
        self.right = right

def distancia_euclidiana(u1: Ubicacion, u2: Ubicacion) -> float:
    distancia = math.sqrt((u2[0] - u1[0])**2 + (u2[1] - u1[1])**2)
    return distancia

def matriz(ubicaciones: list[Ubicacion]) -> list:
    matriz = []
    for i in ubicaciones:
        fila = []
        for j in ubicaciones:
            distancia = distancia_euclidiana(i, j)
            fila.append(distancia)
        matriz.append(fila)
    return matriz

UBICACIONES = [(3.0, 4.0), (1.0, 2.0)]

matriz_1 = matriz(UBICACIONES)
print(f'{matriz_1}')