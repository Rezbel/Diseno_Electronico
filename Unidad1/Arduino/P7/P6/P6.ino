int sensor = A0;
int actuador = 6;

void setup() {
  Serial.begin (9600);
}
int v;
void loop() {
  v=analogRead(sensor);
  v=map(v,0,1023,0,255);
  analogWrite(actuador,v);
  delay(1000);
  }
