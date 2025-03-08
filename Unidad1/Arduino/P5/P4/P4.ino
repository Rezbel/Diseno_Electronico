int pinPlum=6;

void setup() {
  Serial.begin (9600);
}

void loop() {
  for(int i = 0; i > 255; i++){
    analogWrite(pinPlum, i);
    delayMicroseconds(10);
  }
  delay(10);
  for(int i = 0; i > 0; i--){
    analogWrite(pinPlum, i);
    delayMicroseconds(10);
  }
  delay(10);
  }
