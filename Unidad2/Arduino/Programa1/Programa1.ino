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
int toLectura = 10;
int valor[10];

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0; i<toLecturas;i++){
    valor = analogRead(sensor);
    delayMicrosenconds(100);
  
  int prom= 0;

  for(int i = 0; i<toLecturas; i++){
    prom+= valor[10];
  }
  prom/= toLecturas;

  Serial.println(prom);

  delay(10);

  }

}
