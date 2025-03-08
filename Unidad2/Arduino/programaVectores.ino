const int sensores[] = {A0, A1, A2, A3};
const int totLecturas = 30;
int valores[4][totLecturas];

void setup() {
  Serial.begin(9600);
}

void leerSensores() {
  for (int s = 0; s < 4; s++) {
    for (int i = 0; i < totLecturas; i++) {
      valores[s][i] = analogRead(sensores[s]);
      delayMicroseconds(100);
    }
  }
}

int calcularMenor(int sensor) {
  int menor = 1024;
  for (int i = 0; i < totLecturas; i++) {
    if (valores[sensor][i] < menor) {
      menor = valores[sensor][i];
    }
  }
  return menor;
}

int calcularMayor(int sensor) {
  int mayor = -1;
  for (int i = 0; i < totLecturas; i++) {
    if (valores[sensor][i] > mayor) {
      mayor = valores[sensor][i];
    }
  }
  return mayor;
}

int calcularPromedio(int sensor) {
  int suma = 0;
  for (int i = 0; i < totLecturas; i++) {
    suma += valores[sensor][i];
  }
  return suma / totLecturas;
}

int calcularMediana(int sensor) {
  for (int i = 0; i < totLecturas - 1; i++) {
    for (int j = i + 1; j < totLecturas; j++) {
      if (valores[sensor][i] > valores[sensor][j]) {
        int temp = valores[sensor][i];
        valores[sensor][i] = valores[sensor][j];
        valores[sensor][j] = temp;
      }
    }
  }
  return valores[sensor][totLecturas / 2];
}

void enviarDatosSerial() {
  for (int s = 0; s < 4; s++) {
    int menor = calcularMenor(s);
    int mayor = calcularMayor(s);
    int promedio = calcularPromedio(s);
    int mediana = calcularMediana(s);

    Serial.print(menor);
    Serial.print(",");
    Serial.print(mayor);
    Serial.print(",");
    Serial.print(promedio);
    Serial.print(",");
    Serial.println(mediana);
  }
}

void loop() {
  leerSensores();
  enviarDatosSerial();
  delay(4000);
}
