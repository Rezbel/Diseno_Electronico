import time
import serial
import numpy as np
import math
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
def leer_datos(archivo="24hrs.csv"):
    with open(archivo, 'r') as file:
        data = []
        for line in file.readlines():
            try:
                data.append([float(x) for x in line.strip().split(',')])  # Convertir valores a float
            except ValueError:
                print(f"Ignorando línea inválida: {line.strip()}")
    return data

def calcular_iqr(dataset):
    dataset_sorted = sorted(dataset)

    posQ1 = 1 * (len(dataset_sorted) - 1) / 4 + 1
    posQ3 = 3 * (len(dataset_sorted) - 1) / 4 + 1

    def interpolar(q, dataset):
        p_decimal, p_entera = math.modf(q)
        p_entera = int(p_entera)
        return dataset[p_entera - 1] + p_decimal * (dataset[p_entera] - dataset[p_entera - 1])

    Q1 = interpolar(posQ1, dataset_sorted)
    Q3 = interpolar(posQ3, dataset_sorted)

    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    return lower_limit, upper_limit

def limpiar_datos(data):
    column_data = [row[0] for row in data if isinstance(row[0], (int, float))]

    for i in range(1, len(column_data) - 1):
        if column_data[i] in [None, '', ' ']:
            column_data[i] = column_data[i - 1] + (
                    (column_data[i + 1] - column_data[i - 1]) / ((i + 1) - (i - 1))) * (i - (i - 1))

    lower_limit, upper_limit = calcular_iqr(column_data)
    datos_limpios = [row for row in data if lower_limit <= row[0] <= upper_limit]

    return datos_limpios

def proc_ses(vector, dia=1):
    modelo = ARIMA(vector, order=(2, 1, 2))  # ARIMA(2,1,2)
    modelo_ajustado = modelo.fit()

    n_vector = modelo_ajustado.fittedvalues.tolist()
    s_valor = []

    for i in range(len(n_vector)):
        n_valor = n_vector[i]
        if n_valor > 27.5:
            s_valor.append(f"{i + 1}: Prender AC")
        else:
            s_valor.append(f"{i + 1}: Apagar AC")

    return n_vector, s_valor

def main(archivo="24hrs.csv"):
    ser = serial.Serial('COM6', 9600)
    dia = 1
    data = leer_datos(archivo)

    while True:
        print(f"\nDia {dia}")

        if dia == 1:
            vector = [float(row[0]) for row in data]
            print(f"Datos originales del lunes: {vector}")
        else:
            cleaned_data = limpiar_datos(data)
            vector = [float(row[0]) for row in cleaned_data]
            print(f"Datos limpios (dia {dia}): {vector}")

        n_vector, s_valor = proc_ses(vector, dia=dia)

        print(f"\nValores procesados del dia {dia}: {n_vector}")
        print(f"Estado del AC en el dia {dia}: {s_valor}")
        for hora, estado in enumerate(s_valor, start=1):
            print(f"{estado}")
            if 'Prender' in estado:
                ser.write(b'1')
            else:
                ser.write(b'0')
            time.sleep(1)

        dia += 1
        if dia == 8:
            dia = 1

        time.sleep(10)
if __name__ == "__main__":
    main()
