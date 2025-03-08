import serial
import csv
from datetime import datetime
import time

ser = serial.Serial('COM10', 9600)
ser.flush()

with open('datos.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Fecha y Hora', 'Temperatura (°C)', 'Humedad (%)'])

    start_time = time.time()
    while time.time() - start_time < 43200:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            temp, hum = line.split(',')
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([fecha_hora, temp, hum])
            print(f'Registro guardado: {fecha_hora}, Temp: {temp}°C, Humedad: {hum}%')
