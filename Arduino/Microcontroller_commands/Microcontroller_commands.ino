#include <Servo.h>
bool w_sequence_done = false;

const int RIGHT_SENSOR = 6;   // sends 'r'
const int LEFT_SENSOR  = 7;   // sends 'l'
const int BUTTON_PIN = 7;
const int IN1 = 3;
const int IN2 = 2;

const char FSIG = 'q';  // Señal hacia RPi

char motorState = '\0';
char servoState = '\0';

Servo myServo;

const unsigned long DEBOUNCE_TIME = 150;
unsigned long lastPressTime = 0;

long readSensor(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin, LOW);

  pinMode(pin, INPUT);
  long duration = pulseIn(pin, HIGH, 30000);
  pinMode(pin, OUTPUT);

  return duration / 58;
}

void setup() {
  pinMode(RIGHT_SENSOR, OUTPUT);
  pinMode(LEFT_SENSOR, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  myServo.attach(4);  // Servo en pin 4 (ajusta si lo necesitas)

  Serial.begin(115200);
  delay(100);
}

void loop() {
  long rightDist = readSensor(RIGHT_SENSOR);
  long leftDist  = readSensor(LEFT_SENSOR);

  // Si derecha < 15 cm => mandar 'r'
  if (rightDist > 0 && rightDist < 15) {
    Serial.write('r');
    delay(50);
  }

  // Si izquierda < 15 cm => mandar 'l'
  if (leftDist > 0 && leftDist < 15) {
    Serial.write('l');
    delay(50);
  }


  // ---- BOTÓN: enviar 'q' ----
  bool pressed = !digitalRead(BUTTON_PIN);
  if (pressed && (millis() - lastPressTime) > DEBOUNCE_TIME) {
    Serial.write(FSIG);
    lastPressTime = millis();
  

  // ---- LECTURA SERIAL ----
  if (Serial.available()) {
    char incoming = Serial.read();

    // Motor DC
    if (incoming == 'w' || incoming == 'x') {
      motorState = incoming;
    }

    // Servo motor
    if (incoming == 'l' || incoming == 'r' || incoming == 'c') {
      servoState = incoming;
    }
  }

  // ---- CONTROL MOTOR DC ----
  switch (motorState) {
case 'w':  
  if (!w_sequence_done) {
    // Ejecuta la secuencia SOLO UNA VEZ


    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);

    // Marcar como ejecutada
    w_sequence_done = true;
  }

  // *** MODO ADELANTE CONTINUO ***
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  break;


    case 'x':  // Stop
    default:
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      break;
  }

  // ---- CONTROL SERVO ----
  switch (servoState) {
    case 'l':
      myServo.write(0);   // izquierda
      break;

    case 'r':
      myServo.write(180); // derecha
      break;

    case 'c':
    default:
      myServo.write(90);  // centro
      break;
  }
}
}

