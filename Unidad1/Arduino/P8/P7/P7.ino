int sensor = A0;
int actuador = 6;

void setup() {
  Serial.begin (9600);
}
int v;
void loop() {
  v=digitalRead(sensor);
  v= v/4;
  analogWrite(actuador,v);
  delay(1000);
  }
