import numpy as np
import time
import serial
import math
def calcular_iqr(datos):
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    q1_idx = (n + 1) / 4
    q3_idx = 3 * (n + 1) / 4
    def interpolar_q(idx):
        entero, decimal = divmod(idx, 1)
        entero = int(entero) - 1
        return datos_ordenados[entero] + decimal * (datos_ordenados[entero + 1] - datos_ordenados[entero])

    Q1, Q3 = interpolar_q(q1_idx), interpolar_q(q3_idx)
    IQR = Q3 - Q1
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
def limpiar_datos(datos):
    datos_numericos = [float(d) for d in datos]
    lim_inf, lim_sup = calcular_iqr(datos_numericos)
    return [d for d in datos_numericos if lim_inf <= d <= lim_sup]
def proc_ses(datos, alfa=0.7):
    suavizados = [datos[0]]
    decisiones = []
    for i in range(1, len(datos)):
        nuevo_valor = alfa * datos[i] + (1 - alfa) * suavizados[-1]
        suavizados.append(nuevo_valor)
        decisiones.append("Prender AC" if nuevo_valor > 30.5 else "Apagar AC")
    return suavizados, decisiones
def leer_temperaturas(ser, cantidad=24):
    datos = []
    while len(datos) < cantidad:
        if ser.in_waiting > 0:
            temp = ser.readline().decode('utf-8').strip()
            if temp.replace('.', '', 1).isdigit():
                datos.append(float(temp))
                print(f"Temperatura leída: {temp}°C")
            else:
                print("Dato inválido, ignorando...")
    return datos
def enviar_comandos(ser, decisiones):
    for decision in decisiones:
        ser.write(b'1' if "Prender" in decision else b'0')
        print(decision)
        time.sleep(1)
def main():
    ser = serial.Serial('COM6', 9600)
    dia = 1
    while True:
        print(f"\nDía {dia}")
        datos = leer_temperaturas(ser)
        datos_filtrados = limpiar_datos(datos)
        datos_suavizados, decisiones = proc_ses(datos_filtrados)
        enviar_comandos(ser, decisiones)

        dia = dia + 1 if dia < 7 else 1
        time.sleep(10)
if __name__ == "__main__":
    main()
