#include "Servo.h"

int TRIGGER_1 = 12;
int ECHO_1 = 11;

int TRIGGER_2 = 9;
int ECHO_2 = 8;

int SERVO_1 = 2;
int SERVO_2 = 3;

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  
  Serial.println("Iniciando placa...");

  servo1.attach(SERVO_1);
  servo2.attach(SERVO_2);

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
    servo1.write(90);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    servo2.write(90);
  } else {
    Serial.println("Objeto lejos de la placa.");
    servo1.write(0);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    //servo2.write(180);
  }
  
  delay(2000);
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