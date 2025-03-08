import random
def generar_vector(n, rango):
    return [random.randint(*rango) for _ in range(n)]
def calcular_valor_objetivo(vector):
    return sum(x ** 2 for x in vector)
def generar_poblacion(m, n, rango):
    return [generar_vector(n, rango) for _ in range(m)]
def seleccion_mejores(vectores, num_padres):
    vectores.sort(key=calcular_valor_objetivo)
    return vectores[:num_padres]
def cruza_mitad(padres):
    hijos = []
    for i in range(0, len(padres), 2):
        if i + 1 < len(padres):
            corte = len(padres[i]) // 2
            hijo1 = padres[i][:corte] + padres[i+1][corte:]
            hijo2 = padres[i+1][:corte] + padres[i][corte:]
            hijos.extend([hijo1, hijo2])
    return hijos

def mutacion(hijos, rango, probabilidad=20):
    for hijo in hijos:
        if random.randint(1, 100) <= probabilidad:
            i = random.randint(0, len(hijo) - 1)
            hijo[i] = random.randint(*rango)
    return hijos
def seleccion_nueva_generacion(poblacion, num_mejores):
    poblacion.sort(key=calcular_valor_objetivo)
    return poblacion[:num_mejores]

m, n = 10, 5
rango = (1, 10)
num_generaciones = 5
poblacion = generar_poblacion(m, n, rango)
for generacion in range(num_generaciones):
    print(f"\nGeneración {generacion + 1}")
    padres = seleccion_mejores(poblacion, m // 2)
    hijos = cruza_mitad(padres)
    hijos_mutados = mutacion(hijos, rango)
    poblacion = seleccion_nueva_generacion(padres + hijos_mutados, m)
    for ind in poblacion:
        print(ind, "VO:", calcular_valor_objetivo(ind))
