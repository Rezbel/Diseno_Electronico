int sensor = A0;

void setup() {
  Serial.begin (9600);
  }
int v;
void loop() {
  
    v = analogRead(sensor);
    Seria.println("valor="+String(v));
    delay(500); 
   }
  }
