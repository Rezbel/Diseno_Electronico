//PREPROCESAMIENTO DE DATOS...
//
//NORMALMENTE LEEMOS UNICAMENTE UNA VEZ CADA SENSOR Y MANDAMOS
//LA INFORMACION AL PUERTO SERIAL...
//
//ESTO ES INCORRECTO DEBIDO A QUE PODRIAN GENERARSE
//INCONSISTENCIAS EN LAS LECTURAS, POR LO QUE DEBE BUSCARSE 
//TRATA DE AMINORAR ESTA SITUACION MEDIANTE EL PREPROCESAMIENTO...
//
//PRIMERA APROXIMACION.... MEDIDAS DE TENDENCIAS CENTRAL....
//
int sensor = A0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}
int toLecturas = 30;
int valor[30];

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0; i<toLecturas;i++){
    valor[i] = analogRead(sensor);
    delayMicroseconds(100);
  }

  for(int i = 0; i<toLecturas; i++){
    for (int j = i + 1; j < toLecturas; j++) {
      if(valor[valor[j]< valor[i]]){
        int temp = valor[i];
        valor[i] = valor[j];
        valor[j] = temp;
      }
    }
  }
  //ejercicio 1 moda
Serial.println(valor[toLecturas/2]);
  delay(10);
  }