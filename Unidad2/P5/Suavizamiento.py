import numpy as np
import time

def leer_datos(archivo="24hrs.csv"):
    with open(archivo, 'r') as file:
        data = [float(line.strip()) for line in file.readlines()]
    return np.array(data)
def calc_suavizado_exponencial(serie, alfa):
    new_serie = np.zeros(len(serie))
    new_serie[0] = serie[0]
    for t in range(1, len(serie)):
        new_serie[t] = alfa * serie[t] + (1 - alfa) * new_serie[t - 1]
    return new_serie
def controlar_ac(serie, alfa=0.7, umbral=27.5):
    serie_suavizada = calc_suavizado_exponencial(serie, alfa)
    estados_ac = []
    for i, valor in enumerate(serie_suavizada):
        estado = "Prender" if valor > umbral else "Apagar"
        estados_ac.append(f"Hora {i + 1}: {estado}")

    return serie_suavizada, estados_ac
def main(archivo="24hrs.csv"):
    datos = leer_datos(archivo)

    dia = 1
    while dia <= 7:
        print(f"\nDía {dia}")

        serie_suavizada, estados_ac = controlar_ac(datos)

        print("\nValores suavizados:")
        print(serie_suavizada)

        print("\nEstado del AC:")
        for estado in estados_ac:
            print(estado)
            time.sleep(1)
        dia += 1
        time.sleep(3)
    print("\nFin de la semana.")
if __name__ == "__main__":
    main()
