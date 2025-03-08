import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# Cargar datos
file_path = 'capturas.csv'
df = pd.read_csv(file_path, encoding='latin1')

# Renombrar columna de temperatura
df.rename(columns={'Temperatura (°C)': 'Temperatura (C)'}, inplace=True)

# Eliminar valores vacíos con interpolación lineal
df['Temperatura (C)'] = df['Temperatura (C)'].interpolate(method='linear')

# Identificar outliers con el método IQR
Q1 = df['Temperatura (C)'].quantile(0.25)
Q3 = df['Temperatura (C)'].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Tratar outliers reemplazándolos con interpolación lineal
df['Temperatura (C)'] = np.where(
    (df['Temperatura (C)'] < lower_limit) | (df['Temperatura (C)'] > upper_limit),
    np.nan,
    df['Temperatura (C)']
)
df['Temperatura (C)'] = df['Temperatura (C)'].interpolate(method='linear')

# Aplicar modelo ARIMA (p,d,q)
order = (1, 1, 1)  # Hiperparámetros ARIMA, ajustables
modelo = ARIMA(df['Temperatura (C)'], order=order)
ajuste = modelo.fit()

# Generar pronóstico
pronostico = ajuste.forecast(steps=1)  # Un paso adelante
print(f"Pronóstico de temperatura para el siguiente paso: {pronostico.iloc[0]}")