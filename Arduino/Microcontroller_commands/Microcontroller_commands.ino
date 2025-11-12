#include <RotaryEncoder.h>
#include <Servo.h>

#define TurnButton 7  // Turn on button pin

const int IN2 = 2;
const int IN1 = 3;

const char DCST = 'A';  // Motor forward
const char DCB  = 'B';  // Motor backward
const char DCS  = 'C';  // Motor stop
const char DL   = 'D';  // Dodge left
const char DR   = 'E';  // Dodge right
const char CCH  = 'Z';  // Confirm
const char FSIG = 'q';  // Signal sent when button pressed

Servo D;

long DU;
int DICM;
long RT = 0;
long LT = 0;
int posicion_anterior = 0;
int posicion_actual = 0;
char command = '\0';

void setup() {
  D.attach(4);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(TurnButton, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  static bool estadoAnterior = HIGH;
  bool estadoActual = digitalRead(TurnButton);

  if (estadoAnterior == HIGH && estadoActual == LOW) {
    Serial.write(FSIG);   
  }

  estadoAnterior = estadoActual;
}

void serialEvent() {
  while (Serial.available()) {
    command = (char)Serial.read();

    Serial.print("Comando recibido: ");
    Serial.println(command);
    
    switch (command) {
      case DCST:

        break;

      case DCB:

        break;

      default:
        break;
    }
  }
}

