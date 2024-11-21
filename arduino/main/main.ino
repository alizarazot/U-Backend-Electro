#include "Servo.h"

// Por razones súper técnicas, el ultrasonido uno está al lado del servo 2.
// Igualmente, el ultrasonido dos está al lado del servo 1.

int TRIGGER_1 = 12;
int ECHO_1 = 11;

int TRIGGER_2 = 9;
int ECHO_2 = 8;

int SERVO_1 = 2;
int SERVO_2 = 3;

Servo servo1;
Servo servo2;

int SERVO_1_HORIZONTAL = 85;
int SERVO_1_VERTICAL = 0;

int SERVO_2_HORIZONTAL = 87;
int SERVO_2_VERTICAL = 180;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // Esperar a que el puerto serial esté disponible.
  }
  Serial.println("# Iniciando placa...");

  Serial.setTimeout(100000000);  // 27 hours.

  servo1.attach(SERVO_1);
  servo2.attach(SERVO_2);
  servo1.write(SERVO_1_HORIZONTAL);
  servo2.write(SERVO_2_HORIZONTAL);

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(TRIGGER_1, OUTPUT);
  pinMode(TRIGGER_2, OUTPUT);

  pinMode(ECHO_1, INPUT);
  pinMode(ECHO_2, INPUT);

  Serial.println("# Placa configurada!");
  Serial.println("READY");
}

void loop() {
  String command = readCommand();

  if (command == "SKIP") {
    return;
  }

  if (command == "SERVO1" || command == "SERVO2") {
    String direction = readCommand();

    if (command == "SERVO1") {
      if (direction == "HORIZONTAL") {
        servo1.write(SERVO_1_HORIZONTAL);
        return;
      }
      if (direction == "VERTICAL") {
        servo1.write(SERVO_1_VERTICAL);
        return;
      }
    }

    if (command == "SERVO2") {
      if (direction == "HORIZONTAL") {
        servo2.write(SERVO_2_HORIZONTAL);
        return;
      }
      if (direction == "VERTICAL") {
        servo2.write(SERVO_2_VERTICAL);
        return;
      }
    }
  }

  if (command == "LED") {
    String status = readCommand();

    if (status == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      return;
    }

    if (status == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      return;
    }
  }

  if (command == "DISTANCE") {
    unsigned long distance1 = getDistanceUltrasonic(TRIGGER_1, ECHO_1);
    unsigned long distance2 = getDistanceUltrasonic(TRIGGER_2, ECHO_2);

    Serial.println(distance1);
    Serial.println(distance2);
  }
}

String readCommand() {
  Serial.println("# Esperando entrada...");
  String str = Serial.readStringUntil('\n');
  return str.substring(0, str.length());
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
  unsigned long SOUND_VELOCITY = 34300;  // cm/s
  return ((time_us * 0.000001) * SOUND_VELOCITY) / 2;
}
