#include "Servo.h"

int TRIGGER_1 = 12;
int ECHO_1 = 11;

int TRIGGER_2 = 9;
int ECHO_2 = 8;

Servo servo;

void setup() {
  Serial.begin(9600);
  
  Serial.println("Iniciando placa...");

  servo.attach(2);
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(TRIGGER_1, OUTPUT);
  pinMode(TRIGGER_2, OUTPUT);

  pinMode(ECHO_1, INPUT);
  pinMode(ECHO_2, INPUT);

  Serial.println("Placa configurada!");
}

void loop() {
  unsigned long distance1 = getDistanceUltrasonic(TRIGGER_1, ECHO_1);
  unsigned long distance2 = getDistanceUltrasonic(TRIGGER_2, ECHO_2);
  
  Serial.print("Distancia en sensor 1: ");
  Serial.println(distance1);
  
  Serial.print("Distancia en sensor 2: ");
  Serial.println(distance2);
  
  if (distance1 < 10 || distance2 < 10) {
    Serial.println("Objeto cerca de la placa.");
    digitalWrite(LED_BUILTIN, HIGH);
    servo.write(90);
    delay(500);
    servo.write(0);
  } else {
    Serial.println("Objeto lejos de la placa.");
    digitalWrite(LED_BUILTIN, LOW);
    servo.write(180);
  }
  
  delay(1500);
}

// Retorna la distancia en centímetros.
unsigned long getDistanceUltrasonic(int trigger, int echo) {
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  
  unsigned long time = pulseIn(echo, HIGH);
  
  return calcDistance(time);
}

// Retorna la distancia en centímetros.
unsigned long calcDistance(unsigned long time_us) {
  unsigned long SOUND_VELOCITY = 34300; // cm/s
  return ((time_us * 0.000001) * SOUND_VELOCITY) / 2;
}
