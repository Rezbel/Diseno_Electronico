import serial
import pandas as pd
class Lectura:
    def __init__(self, puerto="COM6", baudrate=9600, timeout=1):
        self.puerto = puerto
        self.baudrate = baudrate
        self.timeout = timeout

    def leer_arduino(self):
        with serial.Serial(port=self.puerto, baudrate=self.baudrate, timeout=self.timeout) as arduino:
            while True:
                try:
                    a = arduino.readline().decode('utf-8', errors='ignore').strip()
                    datos = [int(x) for x in a.split('-')] if a else None
                    if datos and len(datos) == 6:
                        return datos
                except (UnicodeDecodeError, ValueError):
                    continue

    def generar_matriz(self, n):
        matriz = []
        intentos = 0
        while len(matriz) < n and intentos < n * 2:
            datos = self.leer_arduino()
            if datos:
                matriz.append(datos)
            intentos += 1
        return matriz

    def calcular_desviacion(self, matriz):
        if not matriz:
            print("No hay datos para calcular desviaciones.")
            return None

        df = pd.DataFrame(matriz, columns=["V1", "V2", "V3", "V4", "V5", "V6"])
        df['Desviacion_Fila'] = df.std(axis=1, ddof=1)
        desviacion_columnas = df.std(axis=0, ddof=1).tolist()
        df.loc[len(df)] = desviacion_columnas + [None]
        return df

    def guardar_matriz_csv(self, df, filename):
        if df is not None:
            df.to_csv(filename, index=False)
            print(f"Datos guardados en {filename}")
        else:
            print("No se guardaron datos porque el DataFrame está vacío.")


if __name__ == "__main__":
    lectura = Lectura()
    matriz = lectura.generar_matriz(100)
    df = lectura.calcular_desviacion(matriz)
    lectura.guardar_matriz_csv(df, "Permutacion_1.csv")
