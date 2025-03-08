#include <DHT.h>

#define DHTPIN 7      // Pin digital donde está conectado el DHT11
#define DHTTYPE DHT11 // Definimos el tipo de sensor

DHT dht(DHTPIN, DHTTYPE);

const int totLecturas = 30;
float tempValores[totLecturas];
float humValores[totLecturas];

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void leerSensores() {
  for (int i = 0; i < totLecturas; i++) {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    // Verificar si la lectura es válida
    if (isnan(temp) || isnan(hum)) {
      Serial.println("Error al leer el DHT11");
      tempValores[i] = 0;
      humValores[i] = 0;
    } else {
      tempValores[i] = temp;
      humValores[i] = hum;
    }

    delay(15000); // Esperar 15 segundos
  }
}

float calcularMediana(float valores[]) {
  // Ordenar los valores
  for (int i = 0; i < totLecturas - 1; i++) {
    for (int j = i + 1; j < totLecturas; j++) {
      if (valores[i] > valores[j]) {
        float temp = valores[i];
        valores[i] = valores[j];
        valores[j] = temp;
      }
    }
  }
  // Retornar la mediana
  return valores[totLecturas / 2];
}

void enviarDatosSerial() {
  float medianaTemp = calcularMediana(tempValores);
  float medianaHum = calcularMediana(humValores);

  Serial.print("Mediana Temperatura: ");
  Serial.print(medianaTemp);
  Serial.print(" C, Mediana Humedad: ");
  Serial.print(medianaHum);
  Serial.println(" %");

  // Formato CSV para Python
  Serial.print(medianaTemp);
  Serial.print(",");
  Serial.println(medianaHum);
}

void loop() {
  leerSensores();
  enviarDatosSerial();
}
