import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def leer_datos(archivo="2da Lectura.csv"):
    try:
        df = pd.read_csv(archivo)

        if 'Temperatura (C)' in df.columns:
            return df['Temperatura (C)'].dropna().tolist()  # Eliminamos valores NaN
        else:
            print("Columna de Temperatura no encontrada en el archivo.")
            return []

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")
        return []
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []


def calcular_iqr(dataset):
    dataset.sort()
    posQ1 = 1 * (len(dataset) - 1) / 4 + 1
    posQ3 = 3 * (len(dataset) - 1) / 4 + 1

    def interpolar(pos, data):
        decimales, enteros = np.modf(pos)
        enteros = int(enteros)
        return data[enteros - 1] + decimales * (data[enteros] - data[enteros - 1])

    Q1 = interpolar(posQ1, dataset)
    Q3 = interpolar(posQ3, dataset)

    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    print(f"Limite IQR: Inferior = {lower_limit}, Superior = {upper_limit}")
    return lower_limit, upper_limit


def interpolacionLineal(data):
    return np.interp(range(len(data)),
                     np.where(data != '')[0],
                     np.array(data)[data != ''])


def limpiar_datos(data):
    data = np.array([float(i) if i != '' else np.nan for i in data])

    data_interpolada = np.interp(range(len(data)),
                                 np.where(np.isnan(data) == False)[0],
                                 data[~np.isnan(data)])

    plt.boxplot(data_interpolada)
    plt.title("Ver outliers")
    plt.show()

    lower_limit, upper_limit = calcular_iqr(data_interpolada)

    data_limpia = np.where((data_interpolada < lower_limit) | (data_interpolada > upper_limit),
                           np.nan, data_interpolada)

    mean_value = np.nanmean(data_limpia)
    data_limpia = np.nan_to_num(data_limpia, nan=mean_value)

    return data_limpia


def procedimientoSuavExpSimp(vector, alfa=0.7):
    nVector = [vector[0]]
    for i in range(1, len(vector)):
        nValor = alfa * vector[i] + (1 - alfa) * nVector[i - 1]
        nVector.append(nValor)
    return nVector


if __name__ == "__main__":
    datos = leer_datos()
    datos_limpios = limpiar_datos(datos)
    valores_suavizados = procedimientoSuavExpSimp(datos_limpios)

    plt.plot(datos_limpios, label="Datos Ajustados")
    plt.plot(valores_suavizados, label="Serie Suavizada", linestyle='dashed')
    plt.legend()
    plt.title("Transformación de Datos: Limpieza y Suavizado")
    plt.show()
