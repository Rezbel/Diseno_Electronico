import serial
import csv
from datetime import datetime
import time

class LecturaDeDatos:
    def leer_arduino(self, puerto="COM10", baudrate=9600):
        arduino = serial.Serial(puerto, baudrate)
        arduino.flush()
        while True:
            if arduino.in_waiting > 0:

                line = arduino.readline().decode('utf-8').rstrip()
                try:
                    pot1, pot2, pot3 = line.split(',')
                    return [int(pot1), int(pot2), int(pot3)]
                except ValueError:
                    pass

    def valor_objetivo(self, vector):
        return sum(x ** 2 for x in vector)

    def generar_vector(self):
        V = self.leer_arduino()
        vo = self.valor_objetivo(V)
        return V, vo

    def generar_matriz(self, M):
        matriz = [self.generar_vector() for _ in range(M)]
        return matriz

    def guardar_csv(self, matriz, archivo_csv):
        with open(archivo_csv, "w", newline="") as f:
            writer = csv.writer(f)
            headers = ["Potenciómetro 1", "Potenciómetro 2", "Potenciómetro 3", "Valor Objetivo (VO)"]
            writer.writerow(headers)
            for vector, vo in matriz:
                writer.writerow(vector + [vo])
        print(f"Población guardada en '{archivo_csv}'")
obj = LecturaDeDatos()
matriz = obj.generar_matriz(10)
obj.guardar_csv(matriz, "potenciometros_datos.csv")