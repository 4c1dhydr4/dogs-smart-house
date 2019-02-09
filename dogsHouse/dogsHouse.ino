/*
  Programa de Control de Casa para Canes Inteligente
    Sensores: 
      PIR - Movimiento: A0
      Sonido: A1
      Temperatura A2
      Motor Abrir: D1
      Motor Cerrar: D2
*/
#include<Servo.h>
const int S1 = A0, S2 = A1, S3 = A2;
const int D1 = 2,D2 = 3;
int s1, s2, s3;
int const DEL = 50, DEL_2 = 500, DEL_LOOP = 100;
String inputString = "";
boolean stringComplete = false;
int times = 0;
Servo puerta;
int pos = 0, puertaPin = 9;


void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  puerta.attach(puertaPin);
}

void loop() {
  event();
  if(times == 200){
    send_data();
    reset();
    times = 0;
  }
  move_sensor(analogRead(S1));
  sound_sensor(analogRead(S2));
  times++;
  delay(DEL_LOOP);
}

void move_sensor(int value){
  if(value > 500){
    s1 = 1023;
  }
}

void sound_sensor(int value){
  if(value > 800){
    s2 = 1023;
  }
}
void reset(){
  s1 = 0;
  s2 = 0;
  s3 = 0;
}
void send_data(){
  Serial.println(crypto());
}

void const_send_data(){
  s1 = analogRead(S1);
  s2 = analogRead(S2);
  s3 = analogRead(S3);
  Serial.println(crypto());
}

String attach_sensorType_value(char sensorLetter,int sensorValue){
  String resultado = "@";
  resultado.concat(sensorLetter);
  resultado.concat(":");
  resultado.concat(sensorValue);
  return resultado;
}

String crypto(){
  String data = "";
  data.concat(attach_sensorType_value('M',s1));
  data.concat(attach_sensorType_value('S',s2));
  data.concat(attach_sensorType_value('T',s3));
  return data;
}
void open_door(){
  digitalWrite(D1,HIGH);
  delay(DEL);
  digitalWrite(D1,LOW);
  digitalWrite(D2,HIGH);
  delay(DEL);
  digitalWrite(D2,LOW);
  delay(3000);
  for(pos = 0; pos <= 120; pos++){
   puerta.write(pos);
   delay(15);
  }
}

void close_door(){
  digitalWrite(D2,HIGH);
  delay(DEL);
  digitalWrite(D2,LOW);
  digitalWrite(D1,HIGH);
  delay(DEL);
  digitalWrite(D1,LOW);
  digitalWrite(D2,HIGH);
  delay(DEL);
  digitalWrite(D2,LOW);
  digitalWrite(D1,HIGH);
  delay(DEL);
  digitalWrite(D1,LOW);
  delay(3000);
  for(pos = 120; pos >= 0; pos--){
   puerta.write(pos);
   delay(15);
  }
}

void event(){
  if (stringComplete) {
    if(inputString == "ODN\n"){
      open_door();
    }
    if(inputString == "CDN\n"){
      close_door();
    }
    inputString = "";
    stringComplete = false;
  }
}
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

