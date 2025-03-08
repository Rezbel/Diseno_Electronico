import time
import serial
import numpy as np
import math
from statsmodels.tsa.arima.model import ARIMA

def leer_datos_serial(ser):
    data = []
    while len(data) < 24:
        if ser.in_waiting > 0:
            temp = ser.readline().decode('utf-8').strip()
            if temp.replace('.', '', 1).isdigit():
                data.append(float(temp))
                print(f"Temperatura leída: {temp}°C")
            else:
                print("Dato no válido")
        else:
            print("Leyendo más datos...")
    return data

def calcular_límites_outliers(datos):
    datos.sort()
    Q1_pos = (len(datos) - 1) * 0.25
    Q3_pos = (len(datos) - 1) * 0.75

    Q1 = datos[int(Q1_pos)] + (Q1_pos % 1) * (datos[int(Q1_pos) + 1] - datos[int(Q1_pos)])
    Q3 = datos[int(Q3_pos)] + (Q3_pos % 1) * (datos[int(Q3_pos) + 1] - datos[int(Q3_pos)])

    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return limite_inferior, limite_superior

def limpiar_datos(datos):
    limite_inferior, limite_superior = calcular_límites_outliers(datos)
    datos_limpios = [d for d in datos if d >= limite_inferior and d <= limite_superior]
    return datos_limpios

def predecir_accion(temperaturas, alfa=0.7):
    modelo = ARIMA(temperaturas, order=(2, 1, 2))
    modelo_ajustado = modelo.fit()
    valores_predichos = modelo_ajustado.fittedvalues.tolist()

    acciones = []
    for i, prediccion in enumerate(valores_predichos):
        if prediccion > 30.5:
            acciones.append(f"{i+1}: Encender AC")
        else:
            acciones.append(f"{i+1}: Apagar AC")
    return valores_predichos, acciones

def control_ac(acciones, ser, previous_estado=""):
    for accion in acciones:
        print(accion)
        if 'Encender' in accion and previous_estado != "Encender":
            ser.write(b'1')  # Comando para encender el AC
            previous_estado = "Encender"
        elif 'Apagar' in accion and previous_estado != "Apagar":
            ser.write(b'0')  # Comando para apagar el AC
            previous_estado = "Apagar"
        time.sleep(1)
    return previous_estado

def main():
    ser = serial.Serial('COM6', 9600)
    dia = 1
    previous_estado = ""

    while True:
        print(f"\nDía {dia}")
        data = leer_datos_serial(ser)

        print(f"\nDatos del día {dia}: {data}")
        data_limpia = limpiar_datos(data)

        predicciones, acciones = predecir_accion(data_limpia)
        print(f"\nPredicciones del día {dia}: {predicciones}")
        print(f"Acciones recomendadas del AC para el día {dia}: {acciones}")
        previous_estado = control_ac(acciones, ser, previous_estado)
        dia += 1
        if dia == 8:
            dia = 1
            print("\nSiguiente semana\n")

        time.sleep(10)

if __name__ == "__main__":
    main()
