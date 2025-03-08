#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0; // Variable para almacenar el tiempo anterior
const long interval = 300000; // Intervalo de 5 minutos en milisegundos

void setup() {
    Serial.begin(9600);
    dht.begin();
}

void loop() {
    unsigned long currentMillis = millis();
    
    // Verificar si ha pasado el intervalo de 5 minutos
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
        
        // Leer temperatura y humedad
        float temp = dht.readTemperature();
        float hum = dht.readHumidity();

        // Verificar si la lectura es válida
        if (isnan(temp) || isnan(hum)) {
            Serial.println("Error al leer el sensor DHT11");
        } else {
            // Enviar datos al puerto serial
            Serial.print(temp);
            Serial.print(",");
            Serial.println(hum);
        }
    }
}
