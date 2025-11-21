#include <Servo.h>

Servo myServo;

const int IN1 = 3;
const int IN2 = 2;
const int BUTTON_PIN = 8;

bool w_sequence_done = false; // desbloquea movimiento
char currentCommand = 'x';    // 'x' = nada, 'w' = avanzar, 'e','v','u' = comandos especiales
unsigned long lastPressTime = 0;
const unsigned long DEBOUNCE_TIME = 150;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  myServo.attach(4);

  Serial.begin(115200);
  delay(100);
}

void loop() {
  // ---------- BOTÓN DE INICIO ----------
  bool pressed = !digitalRead(BUTTON_PIN);
  if (pressed && (millis() - lastPressTime) > DEBOUNCE_TIME) {
    Serial.write('q'); // manda 'q' a la Raspberry
    lastPressTime = millis();
  }

  // ---------- LECTURA SERIAL ----------
  if (Serial.available()) {
    char incoming = Serial.read();

    // SOLO desbloquea movimiento con 'w'
    if (incoming == 'w') {
      w_sequence_done = true;
      currentCommand = 'w'; // empieza a avanzar
    }
    else if (w_sequence_done) {
      // PRIORIDAD: cualquier comando interrumpe movimiento
      if (incoming == 'e' || incoming == 'v' || incoming == 'u') {
        currentCommand = incoming;
      }
    }
  }

  // ---------- EJECUCIÓN DE COMANDOS ----------
  switch (currentCommand) {
    case 'w':
      // Movimiento hacia adelante
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      break;

    case 'e':
      // ------------------------------
      // AQUI VA TU SECUENCIA PARA "e"
      // Combinando motor y servo
      // Por ejemplo:
      // stopMotor();
      // myServo.write(...);
      // digitalWrite(IN1, ...);
      // digitalWrite(IN2, ...);
      // Al finalizar:
      currentCommand = 'w'; // vuelve a avanzar
      break;

    case 'v':
      // ------------------------------
      // AQUI VA TU SECUENCIA PARA "v"
      currentCommand = 'w'; // vuelve a avanzar
      break;

    case 'u':
      // ------------------------------
      // AQUI VA TU SECUENCIA PARA "u"
      currentCommand = 'w'; // vuelve a avanzar
      break;

    default:
      // Stop motor
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      break;
  }

  // ---------- PEQUEÑO RETRASO ----------
  delay(50); // evita saturar loop
}
