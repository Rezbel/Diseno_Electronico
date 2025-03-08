int actuadores[4]= {8,9,10,11}

void setup() {
  Serial.begin (9600);
  for(int i=0; i<4;i++){
    pinMode(actuadores[i],OUTPUT);
  }
}

void loop() {
  for(int i=0; i<4; i++){
    digitalWrite(actuadores[i],1);
    delay(100);

    digitalwrite(actuadores[i],0);
    delay(100);
  }
  delay(1000);
  }
