import serial as conn
import pandas as pd
class Lectura:
    def leer_arduino(self, puerto="COM8", baudrate=9600):
        with conn.Serial(port=puerto, baudrate=baudrate, timeout=1) as arduino:
            try:
                a = arduino.readline().decode('utf-8', errors='ignore').strip()
                print(f"Datos leídos del Arduino: {a}")
                if a:
                    return [int(x) for x in a.split('-')]
                else:
                    print("No se recibió datos válidos.")
                    return None
            except (UnicodeDecodeError, ValueError) as e:
                print(f"Error al procesar datos: {e}")
                return None

    def generar_matriz(self, n):
        matriz = []
        intentos = 0
        while len(matriz) < n and intentos < n * 2:  # Evita intentos infinitos
            print(f"Intento {intentos + 1}...")
            datos = self.leer_arduino()
            if datos and len(datos) == 6:  # Verifica que tenga 6 valores
                matriz.append(datos)
            else:
                print(f"Datos no válidos. Reintentando...")
            intentos += 1
        return matriz

    def calcular_desviacion(self, matriz):
        if matriz:
            df = pd.DataFrame(matriz, columns=["V1", "V2", "V3", "V4", "V5", "V6"])
            df['Desviacion_Fila'] = df.std(axis=1, ddof=1)
            desviacion_columnas = df.std(axis=0, ddof=1).tolist()
            desviacion_fila = pd.DataFrame([desviacion_columnas + [None]],
                                           columns=df.columns)  # Asegura columnas iguales
            df = pd.concat([desviacion_fila, df], ignore_index=True)
            return df
        else:
            print("No se pudo calcular la desviación estándar porque la matriz está vacía.")
            return None

    def guardar_matriz_csv(self, df, filename):
        if df is not None:
            df.to_csv(filename, index=False)
            print(f"Datos guardados en {filename}")
        else:
            print("No se guardaron datos porque el DataFrame está vacío.")


lectura = Lectura()
matriz = lectura.generar_matriz(10)
df = lectura.calcular_desviacion(matriz)
lectura.guardar_matriz_csv(df, 'lecturas.csv')
